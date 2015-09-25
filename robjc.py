#
# R.objc
#
# iOS resource class generator
#
# Copyright (c) 2015 Xoropsax cyrano905@gmail.com (github.com/metasmile)
#

import time
import os
import sys
import re
import textwrap
from os.path import expanduser

if len(sys.argv) == 1:
    print 'usage : python robjc.py [target dir] [destination dir] [class name]'
    sys.exit(0)

__RESOURCE_PATH__ = expanduser(sys.argv[1])
__RESOURCE_CLASS_DEST_PATH__ = expanduser(sys.argv[2]) if len(sys.argv)==3 else './'
__RESOURCE_CLASS__ = sys.argv[3] if len(sys.argv)==4 else 'R'
__DELIMETER__ = '_'
__DELIMETER_ALIAS__ = '='

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

#MARK: file headers
def begin_objc_interface(class_name):
    return textwrap.dedent(
        """\
        #import <objc/NSObject.h>
        @class NSString;

        @interface {0} : NSObject

        """\
    .format(class_name))

def begin_objc_implementation(class_name):
    return textwrap.dedent(
        """\
        #import <Foundation/Foundation.h>
        #import \"{0}.h\"

        @implementation {0}

        """\
    .format(class_name))

def end_objc_file(path, content):
    content += '@end'
    path = path if os.path.isabs(path) else os.path.join(__RESOURCE_PATH__, path)
    f = open(path, 'w')
    f.write(content)
    f.close()
    return content

#MARK: make method strings
def make_method_line(name):
    return '+ (NSString *){0};'.format(name)

def make_method_content(content):
    return textwrap.dedent(
        """\
         {{
            {0}
        }}
        """\
    .format(content))

def make_return_string_line(str_content):
    return 'return @\"{0}\";'.format(str_content)

#
# start main job
#
if __name__ == "__main__":
    start = time.time()

    header_file_content = begin_objc_interface(__RESOURCE_CLASS__)
    impl_file_content = begin_objc_implementation(__RESOURCE_CLASS__)
    cnt = 0

    def append_file(file_name, file):
        _method_line = make_method_line(file_name)

        global header_file_content
        global impl_file_content
        header_file_content += (_method_line + '\n\n')
        impl_file_content += (_method_line + make_method_content(make_return_string_line(file)) + '\n')

    for root, dirs, files in os.walk(__RESOURCE_PATH__):
        cur_dir = os.path.basename(root)
        if not cur_dir:
            continue

        for file_name in files:
            file = os.path.join(root, file_name)

            if check_ignore(file):
                continue

            _file = os.path.basename(file)

            [[append_file(_alias, _file)] for _alias in os.path.splitext(_file)[0].split(__DELIMETER_ALIAS__)]

            cnt+=1

    end_objc_file(os.path.join(__RESOURCE_CLASS_DEST_PATH__, __RESOURCE_CLASS__+'.h'), header_file_content)
    end_objc_file(os.path.join(__RESOURCE_CLASS_DEST_PATH__, __RESOURCE_CLASS__+'.m'), impl_file_content)

print 'all done.', cnt, (time.time() - start)
