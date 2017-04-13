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
import numpy as np
import matplotlib.pyplot as plt

source_folder = '/home/lch/PKU-3D/result/detc/'
ground_folder = '/mnt/hdd/PKUMMD/test_label_0330/'
fig_folder = '/home/lch/PKU-3D/src/fig/'
theta = 0.5 #overlap ratio
number_label = 52

# calc_pr: calculate precision and recall
#	@positive: number of positive proposal
#	@proposal: number of all proposal
#	@ground: number of ground truth
def calc_pr(positive, proposal, ground):
	if (proposal == 0): return 0,0
	if (ground == 0): return 0,0
	return (1.0*positive)/proposal, (1.0*positive)/ground

# match: match proposal and ground truth
#	@lst: list of proposals(label, start, end, confidence, video_name)
#	@ratio: overlap ratio
#	@ground: list of ground truth(label, start, end, confidence, video_name)
#
#	correspond_map: record matching ground truth for each proposal
#	count_map: record how many proposals is each ground truth matched by 
#	index_map: index_list of each video for ground truth
def match(lst, ratio, ground):
	def overlap(prop, ground):
		l_p, s_p, e_p, c_p, v_p = prop
		l_g, s_g, e_g, c_g, v_g = ground
		if (int(l_p) != int(l_g)): return 0
		if (v_p != v_g): return 0
		return (min(e_p, e_g)-max(l_p, l_g))/(max(e_p, e_g)-min(l_p, l_g))

	cos_map = [-1 for x in xrange(len(lst))]
	count_map = [0 for x in xrange(len(ground))]
	#generate index_map to speed up
	index_map = [[] for x in xrange(number_label)]
	for x in xrange(len(ground)):
		index_map[int(ground[x][0])].append(x)

	for x in xrange(len(lst)):
		for y in index_map[int(lst[x][0])]:
			if (overlap(lst[x], ground[y]) < ratio): continue
			if (overlap(lst[x], ground[y]) < overlap(lst[x], ground[cos_map[x]])): continue
			cos_map[x] = y
		if (cos_map[x] != -1): count_map[cos_map[x]] += 1
	positive = sum([(x>0) for x in count_map])
	return cos_map, count_map, positive

# plot_fig: plot precision-recall figure of given proposal
#	@lst: list of proposals(label, start, end, confidence, video_name)
#	@ratio: overlap ratio
#	@ground: list of ground truth(label, start, end, confidence, video_name)
#	@method: method name
def plot_fig(lst, ratio, ground, method):
	lst.sort(key = lambda x:x[3]) # sorted by confidence
	cos_map, count_map, positive = match(lst, ratio, ground)
	number_proposal = len(lst)
	number_ground = len(ground)
	old_precision, old_recall = calc_pr(positive, number_proposal, number_ground)

	recalls = [old_recall]
	precisions = [old_precision] 
	for x in xrange(len(lst)):
		number_proposal -= 1;
		if (cos_map[x] == -1): continue
		count_map[cos_map[x]] -= 1;
		if (count_map[cos_map[x]] == 0) : positive -= 1;

		precision, recall = calc_pr(positive, number_proposal, number_ground)   
		if precision>old_precision: 
			old_precision = precision
		recalls.append(recall)
		precisions.append(old_precision)
		old_recall = recall
	fig = plt.figure()
	plt.axis([0,1,0,1])
	plt.plot(recalls,precisions,'r')  
	plt.savefig('%s%s.png'%(fig_folder,method))
 
# f1-score:
#	@lst: list of proposals(label, start, end, confidence, video_name)
#	@ratio: overlap ratio
#	@ground: list of ground truth(label, start, end, confidence, video_name)
def f1(lst, ratio, ground):
	cos_map, count_map, positive = match(lst, ratio, ground)
	precision, recall = calc_pr(positive, len(lst), len(ground))
	score = 2*precision*recall/(precision+recall)
	return score

# Interpolated Average Precision:
#	@lst: list of proposals(label, start, end, confidence, video_name)
#	@ratio: overlap ratio
#	@ground: list of ground truth(label, start, end, confidence, video_name)
#
#	score = sigma(precision(recall) * delta(recall))
#	Note that when overlap ratio < 0.5, 
#		one ground truth will correspond to many proposals
#		In that case, only one positive proposal is counted
def ap(lst, ratio, ground):
	lst.sort(key = lambda x:x[3]) # sorted by confidence
	cos_map, count_map, positive = match(lst, ratio, ground)
	score = 0;
	number_proposal = len(lst)
	number_ground = len(ground)
	old_precision, old_recall = calc_pr(positive, number_proposal, number_ground)
 
	for x in xrange(len(lst)):
		number_proposal -= 1;
		if (cos_map[x] == -1): continue
		count_map[cos_map[x]] -= 1;
		if (count_map[cos_map[x]] == 0): positive -= 1;

		precision, recall = calc_pr(positive, number_proposal, number_ground)   
		if precision>old_precision: 
			old_precision = precision
		score += old_precision*(old_recall-recall)
		old_recall = recall
	return score

# process: calculate scores for each method
def process(method):
	folderpath = source_folder+method+'/'

	v_props = [] # proposal list separated by video
	v_grounds = [] # ground-truth list separated by video
	
	#========== find all proposals separated by video========
	for video in os.listdir(folderpath):
		prop = open(folderpath+video,'r').readlines()
		prop = [prop[x].replace(",", " ") for x in xrange(len(prop))]
		prop = [[float(y) for y in prop[x].split()] for x in xrange(len(prop))]
		ground = open(ground_folder+video,'r').readlines()
		ground = [ground[x].replace(",", " ") for x in xrange(len(ground))]
		ground = [[float(y) for y in ground[x].split()] for x in xrange(len(ground))]
		#append video name
		for x in prop: x.append(video)
		for x in ground: x.append(video) 
		v_props.append(prop)
		v_grounds.append(ground)

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

	#========== calculate protocols========
	print "================================================"
	print "evaluation for method: %s"%method
	print "---- for theta = %lf"%theta
	print "-------- F1 = ", f1(all_props, theta,all_grounds)
	print "-------- AP = ", ap(all_props, theta,all_grounds)
	print "-------- mAP_action = ", sum([ap(a_props[x+1], theta, a_grounds[x+1]) \
		for x in xrange(number_label-1)])/(number_label-1)
	print "-------- mAP_video = ", sum([ap(v_props[x], theta, v_grounds[x]) \
		for x in xrange(len(v_props))])/len(v_props)
	print "-------- 2DAP = ", sum([ap(all_props, (ratio+1)*0.05, all_grounds) \
		for ratio in xrange(20)])/20

	plot_fig(all_props, theta, all_grounds, method)
	print "==============================================="

if __name__ == '__main__':
	methods = os.listdir(source_folder)
	methods.sort()
	for method in methods:
		process(method)
