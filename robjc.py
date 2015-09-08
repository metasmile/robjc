#
# R.objc
#
# iOS resource class generator
#
# Copyright (c) 2015 Xoropsax cyrano905@gmail.com (github.com/metasmile)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import time
import os
import sys
import re
from os.path import expanduser

if len(sys.argv) == 1:
    print 'usage : python robjc.py [target dir] [destination dir] [class name]'
    sys.exit(0)

__RESOURCE_PATH__ = expanduser(sys.argv[1])
__RESOURCE_CLASS_DEST_PATH__ = expanduser(sys.argv[2]) if len(sys.argv)==3 else './'
__RESOURCE_CLASS__ = sys.argv[3] if len(sys.argv)==4 else 'R'
__DELIMETER__ = '_'

#
# define func
#
def get_splited_first(str, delimeter):
    s_arr = str.split(delimeter)
    if not len(s_arr) > 1: return None
    return s_arr[-1].split(__DELIMETER__)[0]

def check_truncate(file, patt):
    name = os.path.basename(file)
    return name and name.find(__DELETE_FILE_HEAD__) == 0 and (patt.match(name[len(__DELETE_FILE_HEAD__):]) is not None) and os.path.getsize(file)>0

def check_ignore(file):
    return os.path.basename(file).startswith('.') or not os.path.isfile(file) or os.path.getsize(file)<1

def begin_objc_interface(class_name):
    content = '#import <objc/NSObject.h>\n'
    content += '@class NSString;\n\n'
    content += '@interface '+class_name+' : NSObject\n\n'
    return content

def begin_objc_implementation(class_name):
    content = '#import <Foundation/Foundation.h>\n'
    content += '#import "'+class_name+'.h"\n\n'
    content += '@implementation '+class_name+' : NSObject\n\n'
    return content

def end_objc_file(path, content):
    content += '@end'
    path = path if os.path.isabs(path) else os.path.join(__RESOURCE_PATH__, path)
    print path
    f = open(path, 'w')
    f.write(content)
    f.close()
    return content

#
# start main job
#
if __name__ == "__main__":
    start = time.time()

    header_file_content = begin_objc_interface(__RESOURCE_CLASS__)
    impl_file_content = begin_objc_implementation(__RESOURCE_CLASS__)
    cnt = 0

    for root, dirs, files in os.walk(__RESOURCE_PATH__):
        cur_dir = os.path.basename(root)
        if not cur_dir:
            continue

        for file_name in files:
            file = os.path.join(root, file_name)

            if check_ignore(file):
                continue

            _file = os.path.basename(file)
            _file_name = os.path.splitext(_file)[0]
            _method_line = '+ (NSString *)'+_file_name+';'

            header_file_content += _method_line + '\n\n'
            impl_file_content += _method_line + ' {\n    return @"'+_file+'";\n}\n\n'
            cnt+=1

    print end_objc_file(os.path.join(__RESOURCE_CLASS_DEST_PATH__, __RESOURCE_CLASS__+'.h'), header_file_content)
    print end_objc_file(os.path.join(__RESOURCE_CLASS_DEST_PATH__, __RESOURCE_CLASS__+'.m'), impl_file_content)

print 'all done.', cnt, (time.time() - start)
