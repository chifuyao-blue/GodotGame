import h5py
file_path = ('Model\keras_model.h5')
f = h5py.File(file_path, 'r')
for key in f.keys():
    print(f[key])
# f.keys()
# print([key for key in f.keys()])

for key in f:
    print("key:" + key)

