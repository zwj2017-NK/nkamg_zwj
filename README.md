# nkamg_zwj
#2018-09-05\
#Wenjun Zhu\
#1103466626@qq.com

pool.py\
这个脚本主要功能是解释python进程池的妙用，包括map、apply、apply_async、map_async函数等

change_file_and_dir_attribute.py\
将三层文件夹的权限改为744，文件夹内的文件权限改给644

check_sha256.py\
使用多进程检查三层文件夹下文件的sha256和文件名是否一致，每个进程分配一个任务，进程执行完会返回一个列表，程序使用了32个进程，所以每次循环都会返回一个长度为32的列表，列表内的元素还是一个列表，即每个进程执行的结果。

get_feature_list.py\
同样是利用多进程，每个进程检查一个三层目录下所有样本文件是否有相对应的.data文件，如果不存其对应的.data文件，则将它的sha256记录下来，程序结束前将这些sha256的记录写到文件中。

