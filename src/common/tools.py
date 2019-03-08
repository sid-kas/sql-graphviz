import os, threading, sys
import time
import errno
import contextlib
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby
from datetime import datetime
from dateutil.tz import gettz


def now():  
    dt = datetime.now(gettz("Europe/Stockholm")).strftime('%Y-%m-%d %H-%M-%S.%d')[:-3]
    return str(dt.replace(' ','_'))

def get_filepath(dir_ = ".",filterby = ".meta",indx=-1):
    cwd = os.getcwd()
    os.chdir(dir_)
    file_name = list(sorted( os.listdir('.'), key=os.path.getmtime))[indx]
    os.chdir(cwd)
    return dir_ + "/" +file_name

def get_parent_dir(ref = 'tf_app'):
    cwd = os.getcwd()
    dir_l = ['.','..//','..//']
    for d in dir_l:
      os.chdir(d)
      sub_dir = list(next(os.walk('.'))[1])
      if ref in sub_dir:
        ans = os.getcwd()
        os.chdir(cwd)
        return ans


def split_padded(data, windowSize):
    a = np.array(data)
    size = len(a)
    if size%windowSize==0:
        n = int(size/windowSize)
    else:
        n = int(size/windowSize)+1
    padding = -size%windowSize
    split_list = np.split(np.concatenate((a,np.zeros(padding))),n)
    return split_list

def split_data(data, seq_len,verbose=1):
    len_d = len(data)
    indx = (len_d//seq_len)*seq_len
    nSplits = len_d//seq_len
    if verbose==1:
        print("Data loss: ", (len_d-indx))
    x_split = np.split(data[:indx,:],nSplits,axis=0)
    return x_split

def split_seq(df,x_cols, y_cols, seq_len = 128, n_classes = 5):
    labels = df[y_cols[0]].unique()
    n_channels=len(x_cols)

    print("Labels: ", labels)
    nbatches = (len(df)//seq_len)
    x_data = np.zeros((nbatches,seq_len,n_channels))
    y_data = np.zeros((nbatches,n_classes))
    print("x columns: ", x_cols)

    data_n = np.array(df[x_cols+y_cols].values)
    size = np.shape(data_n)[0]
    indx = np.arange(0,size,seq_len)
    print("Data loss: ", (size-indx[-1]))
    rm_indxs = []
    for i,(a,b) in enumerate(zip(indx[:-1], indx[1:])):
        y = data_n[a:b,-1]
        y_l = np.unique(y)
        if len(y_l)>1:
            label = 1
            rm_indxs.append(i)
        else:
            label = y_l[0]
            if label ==-1:
                label = 1
                rm_indxs.append(i)
        x = data_n[a:b,:-1]

        x_data[i,:,:] = x
        y_data[i,:] = np.eye(n_classes)[[int(label)]]

    x_data = np.delete(x_data,rm_indxs,axis=0)
    y_data = np.delete(y_data,rm_indxs,axis=0)
    # x_data = x_data[:b_indx,:,:]; y_data = y_data[:b_indx,:]
    print(np.shape(x_data), np.shape(y_data))
    return x_data, y_data

def get_folder_size(folder_name):
    " works with in the directory of the script"
    script_dir = os.path.dirname(__file__)
    rel_path = folder_name
    abs_folder_path = os.path.join(script_dir, rel_path)
    k = int(sum([entry.stat().st_size for entry in os.scandir(abs_folder_path)])/(1024*1024))
    return k


def mkdir_p(path, folder_name = None):
    if folder_name:
        abs_folder_path = os.path.join(path, folder_name)
    else:
        abs_folder_path = path
    try:
        os.makedirs(abs_folder_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(abs_folder_path):
            pass
        else:
            raise

def one_hot(labels, n_class = 6):
	expansion = np.eye(n_class)
	y = expansion[:, labels-1].T
	assert y.shape[1] == n_class, "Wrong number of labels!"

	return y

def get_batches(x, y, batch_size = 100):
	n_batches = len(x) // batch_size
	x, y = x[:n_batches*batch_size], y[:n_batches*batch_size]

	for b in range(0, len(x), batch_size):
		yield x[b:b+batch_size], y[b:b+batch_size]

class Timer(object):
    def __init__(self,timeout=10):
        self.sessionTime = 0
        self.timeout = timeout
        self.start_time = 0
        self.isStarted = False
    def start(self):
        if not self.isStarted:
            self.start_time = time.time()  
            self.isStarted = True
    def stop(self):
        if self.isStarted:
            self.isStarted = False
    def elapsedTime(self):
        if self.isStarted:
            self.sessionTime = (time.time() - self.start_time)
        return self.sessionTime

    def reset(self):
        self.start_time = 0
        self.isStarted = False       
    def isTimeOut(self):
        if (self.elapsedTime() >= self.timeout) :
            self.reset()
            return True
        elif not self.isStarted:
            return True
        else:
            return False
        
class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
import json         
from collections import namedtuple
def json2obj(data): return json.loads(str(data).replace("\'","\""), object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))


class AttrDict(dict):
  """Wrap a dictionary to access keys as attributes."""

  def __init__(self, *args, **kwargs):
    super(AttrDict, self).__init__(*args, **kwargs)
    super(AttrDict, self).__setattr__('_mutable', False)

  def __getattr__(self, key):
    # Do not provide None for unimplemented magic attributes.
    if key.startswith('__'):
      raise AttributeError
    return self.get(key, None)

  def __setattr__(self, key, value):
    if not self._mutable:
      message = "Cannot set attribute '{}'.".format(key)
      message += " Use 'with obj.unlocked:' scope to set attributes."
      raise RuntimeError(message)
    if key.startswith('__'):
      raise AttributeError("Cannot set magic attribute '{}'".format(key))
    self[key] = value

  @property
  @contextlib.contextmanager
  def unlocked(self):
    super(AttrDict, self).__setattr__('_mutable', True)
    yield
    super(AttrDict, self).__setattr__('_mutable', False)

  def copy(self):
    return type(self)(super(AttrDict, self).copy())


# import tensorflow as tf
# def flatten(tensor):
#     fltlsts = [tf.reshape(y,(tf.reduce_prod(tf.shape(y),axis=0),1)) for y in tensor]
#     return tf.concat(fltlsts,axis=0)

# def unflatten(tensor, shapes):
#     prodShapes = tf.reduce_prod(shapes,axis=1)   
#     tensorSplit =  tf.split(tensor,prodShapes) 
#     return [tf.reshape(tensorSplit[i],ys) for i,ys in enumerate(shapes)]

# def plot_3d(x,y,z,fig_num = 1):
#     fig = plt.figure(num=fig_num, figsize=(8, 8))
#     ax = fig.add_subplot(111,projection='3d')
#     ax.scatter(x,y,z,cmap=plt.cm.Spectral)
#     ax.view_init(4, -72)

# def TensorboardLauncher(log_dir):
#     from tensorboard import main as tb
#     import threading
#     tf.flags.FLAGS.logdir = log_dir
#     t = threading.Thread(target=tb.main, args=([]))
#     t.start()
