# Copyright (c) 2017 Chunhui_Liu@STRUCT_ICST_PKU, All rights reserved.
#
# evaluation protocols used for PKU-MMD dataset
# http://www.icst.pku.edu.cn/struct/Projects/PKUMMD.html
#
# In proposal folder:
#	each file contains results for one video.
#	several lines in one file,
#	each line contain: label, start_frame, end_frame, confidence  

import os
import numpy
import matplotlib.pyplot as plt

source_folder = '/home/lch/PKU-3D/result/detc/'
ground_folder = '/mnt/hdd/PKUMMD/test_label_0330/'
fig_folder = '/home/lch/PKU-3D/src/fig/'
theta = 0.5 #overlap ratio
number_label = 52

# plot_fig: plot precision-recall figure of given proposal
#	@lst: list of proposals(label, start, end, confidence, overlap)
#	@ratio: overlap ratio
#	@total: total number, mainly used for recall
#	@method: method name
def plot_fig(lst, ratio, total,method):
	lst.sort(key = lambda x:x[3])
	pos = sum([int(x[4] >= ratio) for x in lst])*1.0
	number = len(lst)*1.0
	recalls = []
	precisions = []
	for proposal in lst:
		number = number - 1;
		if (proposal[4] < ratio): continue
		pos = pos - 1;
		if (number == 0): break
		recalls.append(str(pos/total))
		precisions.append(str(pos/number))
	fig = plt.figure()
	plt.plot(recalls,precisions,'r')  
	plt.savefig('%s%s.png'%(fig_folder,method))

# f1-score:
#	@lst: list of proposals(label, start, end, confidence, overlap)
#	@ratio: overlap ratio
#	@total: total number, mainly used for recall
def f1(lst, ratio, total):
	pos = sum([int(x[4] >= ratio) for x in lst])*1.0
	number = len(lst)*1.0
	precision = pos/number
	recall = pos/(total*1.0)
	score = 2*precision*recall/(precision+recall)
	return score

# Interpolated Average Precision:
#	@lst: list of proposals(label, start, end, confidence, overlap)
#	@ratio: overlap ratio
#	@total: total number, mainly used for recall
#
#	score = sigma(precision(recall) * delta(recall))
#		  = sigma(precision(recall) * (1/total))
#				for recall = 0/total : total/total
def ap(lst, ratio, total):
	lst.sort(key = lambda x:x[3]) # sorted by confidence
	pos = sum([int(x[4] >= ratio) for x in lst])*1.0 # filtered by overlap 

	score = 0;
	number = len(lst)*1.0
	old_precision = 0
	if (total == 0): return 0
	old_recall = min(pos/total,1)

	for x in lst:
		number = number - 1;
		if (x[4] < ratio): continue
		pos = pos - 1;
		if (number == 0): break
		precision = pos/number
		recall = min(pos/total,1)
		if precision>old_precision: 
			old_precision = precision
		score += old_precision*(old_recall-recall)
		old_recall = recall

	score += old_precision*old_recall;
	return score

# calc_ovlp
#	@proposal: label, start, end, confidence
#	@lst: list of ground-truth proposals
def calc_ovlp(proposal, lst):
	label, start, end, conf = proposal
	overlap = 0.0
	for l,s,e,c in lst:
		if (int(l) != int(label)): continue
		overlap = max(overlap, ((min(e,end)-max(s,start))*1.0)/(1.0*(max(e,end)-min(s,start))))
	return overlap

# process: calculate scores for each method
def process(method):
	folderpath = source_folder+method+'/'

	v_props = [] # proposal list separated by video
	v_grounds = [] # ground-truth list separated by video
	
	#========== find all proposals separated by video========
	for video in os.listdir(folderpath):
		prop = open(folderpath+video,'r').readlines()
		prop = [prop[x].replace(",", " ") for x in xrange(len(prop))]
		prop = [[float(y) for y in prop[x].split()]for x in xrange(len(prop))]

		ground = open(ground_folder+video,'r').readlines()
		ground = [ground[x].replace(",", " ") for x in xrange(len(ground))]
		ground = [[float(y) for y in ground[x].split()] for x in xrange(len(ground))]

		v_props.append(prop)
		v_grounds.append(ground)

   	#========== add overlap info for every proposal ========
	for x in xrange(len(v_props)):
		for y in xrange(len(v_props[x])):
			v_props[x][y].append(calc_ovlp(v_props[x][y],v_grounds[x]))
	
	#========== find all proposals separated by action categories========
	# proposal list separated by class
	a_props = [[] for x in xrange(number_label)]
	# ground-truth list separated by class
	a_grounds = [[] for x in xrange(number_label)]

	for x in xrange(len(v_props)):
		for y in xrange(len(v_props[x])):
			a_props[int(v_props[x][y][0])].append(v_props[x][y])
	
	for x in xrange(len(v_grounds)):
		for y in xrange(len(v_grounds[x])):
			a_grounds[int(v_grounds[x][y][0])].append(v_grounds[x][y])

	#========== find all proposals========
	all_props = sum(a_props,[])
	all_grounds = sum(a_grounds, [])

	#========== count all proposals========
	v_grounds_numer = [len(x) for x in v_grounds]
	a_grounds_number = [len(x) for x in a_grounds]
	all_grounds_number = len(all_grounds)


	#========== calculate protocols========
	print "================================================"
	print "evaluation for method: %s"%method
	print "---- for theta = %lf"%theta
	print "-------- F1 = ", f1(all_props, theta,all_grounds_number)
	print "-------- AP = ", ap(all_props, theta,all_grounds_number)
	print "-------- mAP_action = ", sum([ap(a_props[x],theta,a_grounds_number[x]) \
		for x in xrange(len(a_props))])/len(a_props)
	print "-------- mAP_video = ", sum([ap(v_props[x],theta,v_grounds_numer[x]) \
		for x in xrange(len(v_props))])/len(v_props)
	print "-------- 2DAP = ", sum([ap(all_props, (ratio+1)*0.01, all_grounds_number) \
		for ratio in xrange(100)])/100

	plot_fig(all_props, theta, all_grounds_number,method)
	print "==============================================="

if __name__ == '__main__':
	for method in os.listdir(source_folder):
		process(method)
