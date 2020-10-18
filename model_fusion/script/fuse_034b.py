
# coding: utf-8

# In[1]:


import os
import sys
import pickle
import csv
import numpy as np


# ## Concatenating the results 

# In[3]:


with open('../../results/det_results_m18_kf_oi_1_filtered.pkl', 'rb') as fin:
    det_results_oi = pickle.load(fin)

with open('../../results/det_results_m18_kf_coco_1_filtered.pkl', 'rb') as fin:
    det_results_coco = pickle.load(fin)

with open('../../results/det_results_ws_kf_dpl_034b.pkl', 'rb') as fin:
    det_results_ws = pickle.load(fin)
    
#with open('/home/alireza/aida/rootdir/Ram/M18/main/m18_eval_jpg_voc_detn_fin_results.pkl', 'rb') as fin:
#    det_results_voc = pickle.load(fin)


# In[4]:


with open('../../wsod/metadata/ont_m36/mapping.pkl', 'rb') as fin:
    mid2ont, syn2mid, single_mids, mid2syn, class2ont, ont2name, class_names = pickle.load(fin)  



det_results_concat = {}
for imgid in det_results_oi:
    if imgid not in det_results_concat:
        det_results_concat[imgid] = []
    for det in det_results_oi[imgid]:
        if det['score'] < 0.1:
            continue
        det_results_concat[imgid].append({
            'label': det['label'],
            'score': det['score'],
            'bbox': det['bbox'],
            'bbox_normalized': det['bbox_normalized'],
            'model': 'oi',
        })

for imgid in det_results_coco:
    if imgid not in det_results_concat:
        det_results_concat[imgid] = []
        print("WARNING: image in coco not in oi")
    for det in det_results_coco[imgid]:
        if det['score'] < 0.1:
            continue
        det_results_concat[imgid].append({
            'label': det['label'],
            'score': det['score'],
            'bbox': det['bbox'],
            'bbox_normalized': det['bbox_normalized'],
            'model': 'coco',
        })
                
for imgid in det_results_ws:
    if imgid not in det_results_concat:
        det_results_concat[imgid] = []
        print("WARNING: image in ws not in oi")
    for det in det_results_ws[imgid]:
        if det['score'] < 0.1:
            continue
        det_results_concat[imgid].append({
            'label': det['label'],
            'score': det['score'],
            'bbox': det['bbox'],
            'bbox_normalized': det['bbox_normalized'],
            'model': 'ws',
        })
'''
for imgid in det_results_voc:
    if imgid not in det_results_concat:
        det_results_concat[imgid] = []
        print("WARNING: image in ws not in oi")
    for det in det_results_voc[imgid]:
        if det['score'] < 0.1:
            continue
        det_results_concat[imgid].append({
            'label': det['label'],
            'score': det['score'],
            'bbox': det['bbox'],
            'bbox_normalized': det['bbox_normalized'],
            'model': 'voc',
        })
     

'''

# In[13]:


with open('../../results/det_results_concat_34b.pkl', 'wb') as fout:
    pickle.dump(det_results_concat, fout)


# ## Merging duplicate results

# In[14]:


def iou(det_bbox, gt_bbox):
    x_d_len = det_bbox[2] - det_bbox[0]
    y_d_len = det_bbox[3] - det_bbox[1]
    x_t_len = gt_bbox[2] - gt_bbox[0]
    y_t_len = gt_bbox[3] - gt_bbox[1]
    x_int_len = max(0, min(gt_bbox[2], det_bbox[2]) - max(gt_bbox[0], det_bbox[0]))
    y_int_len = max(0, min(gt_bbox[3], det_bbox[3]) - max(gt_bbox[1], det_bbox[1]))
    iou = (x_int_len*y_int_len) / (x_d_len*y_d_len + x_t_len*y_t_len - x_int_len*y_int_len)
    return iou


def iomin(det_bbox, gt_bbox):
    x_d_len = det_bbox[2] - det_bbox[0]
    y_d_len = det_bbox[3] - det_bbox[1]
    x_t_len = gt_bbox[2] - gt_bbox[0]
    y_t_len = gt_bbox[3] - gt_bbox[1]
    x_int_len = max(0, min(gt_bbox[2], det_bbox[2]) - max(gt_bbox[0], det_bbox[0]))
    y_int_len = max(0, min(gt_bbox[3], det_bbox[3]) - max(gt_bbox[1], det_bbox[1]))
    iom = (x_int_len*y_int_len) / min(x_d_len*y_d_len, x_t_len*y_t_len)
    return iom

# In[15]:


mid2toplevel = {k: v.split('.')[0].split()[0] for k, v in class_names.items()}

_STAT_num_same_merged = 0
_STAT_num_diff_merged = 0

iou_thresh_exact_match = 0.5
iou_thresh_top_level_match = 0.5
iomin_thresh_exact_match = 0.9
iomin_thresh_top_level_match = 0.9

all_groups = {}
for imgid, det in det_results_concat.items():
    groups = []
    for ii in range(len(det)):
        if det[ii]['label'] not in mid2ont:
            continue
        matching_gr = None
        for gr in groups:
            for item in gr:
                if len(set(mid2ont[det[ii]['label']]) & set(mid2ont[det[item]['label']])) > 0 and \
                (iou(det[ii]['bbox'], det[item]['bbox']) > iou_thresh_exact_match or
                 iomin(det[ii]['bbox'], det[item]['bbox']) > iomin_thresh_exact_match):
                    if matching_gr == None:
                        gr.append(ii)
                        matching_gr = gr
                    else:
                        matching_gr += gr
                        gr.clear()
                    _STAT_num_same_merged += 1
                    break
                elif mid2toplevel[det[ii]['label']] == mid2toplevel[det[item]['label']] and \
                (iou(det[ii]['bbox'], det[item]['bbox']) > iou_thresh_top_level_match or
                 iomin(det[ii]['bbox'], det[item]['bbox']) > iomin_thresh_top_level_match):
                    if matching_gr == None:
                        gr.append(ii)
                        matching_gr = gr
                    else:
                        matching_gr += gr
                        gr.clear()
                    _STAT_num_diff_merged += 1
                    break
                
        if matching_gr == None:
            groups.append([ii])
    all_groups[imgid] = groups
            


# In[16]:


mid2level = {mid: len(name.split(' ')[0].split('.')) for mid, name in class_names.items()}


# In[19]:


class_preference = {'voc': 1.0, 'coco': 2.0, 'oi': 3.0, 'ws': 4.0}

det_results_merged = {}
for imgid, groups in all_groups.items():
    det_results_merged[imgid] = []
    det = det_results_concat[imgid]
    for g in groups:
        if len(g) == 0:
            continue
        suff = '/J' if len(g) > 1 else ''

        mod_scores = [det[i]['score'] + (10.0 * class_preference[det[i]['model']]) + (100.0 * mid2level[det[i]['label']]) for i in g]
        imax = np.argmax(mod_scores)
        label = det[g[imax]]['label']
        model = det[g[imax]]['model'] + suff

        boxes = np.stack([det[ii]['bbox'] for ii in g], axis=0)
        box = np.concatenate([boxes[:, :2].min(axis=0), boxes[:, 2:].max(axis=0)])
        boxes = np.stack([det[ii]['bbox_normalized'] for ii in g], axis=0)
        box_norm = np.concatenate([boxes[:, :2].min(axis=0), boxes[:, 2:].max(axis=0)])

        scores = [det[ii]['score'] for ii in g]
        score = np.max(scores)
        
        if score < 0.01:
            continue
        
        det_results_merged[imgid].append({
            'label': label,
            'score': score,
            'bbox': box,
            'bbox_normalized': box_norm,
            'model': model,            
        })


all_groups = {}
for imgid, det in det_results_merged.items():
    groups = []
    g_all = []
    for t in set(mid2toplevel.values()):
        g = [ii for ii in range(len(det)) if mid2toplevel[det[ii]['label']] == t]
        if len(g) >= 10: 
            groups.append(g)
            g_all += g
    groups += [[ii] for ii in range(len(det)) if ii not in g_all]
    all_groups[imgid] = groups



det_results_grouped = {}
for imgid, groups in all_groups.items():
    det_results_grouped[imgid] = []
    det = det_results_merged[imgid]
    for g in groups:
        if len(g) == 0:
            continue
        suff = '/G' if len(g) > 1 else ''

        mod_scores = [det[i]['score'] + (10.0 * class_preference[det[i]['model'].split('/')[0]]) + (100.0 * mid2level[det[i]['label']]) for i in g]
        imax = np.argmax(mod_scores)
        label = det[g[imax]]['label']
        model = det[g[imax]]['model'] + suff

        boxes = np.stack([det[ii]['bbox'] for ii in g], axis=0)
        box = np.concatenate([boxes[:, :2].min(axis=0), boxes[:, 2:].max(axis=0)])
        boxes = np.stack([det[ii]['bbox_normalized'] for ii in g], axis=0)
        box_norm = np.concatenate([boxes[:, :2].min(axis=0), boxes[:, 2:].max(axis=0)])
            
        scores = [det[ii]['score'] for ii in g]
        score = np.max(scores)
        
        if score < 0.01:
            continue
        
        det_results_grouped[imgid].append({
            'label': label,
            'score': score,
            'bbox': box,
            'bbox_normalized': box_norm,
            'model': model,            
        })


# In[20]:


with open('../../results/det_results_merged_34b.pkl', 'wb') as fout:
    pickle.dump(det_results_grouped, fout)

