# R_objc
Simple objective-c resource class generator inspired by android.R.

## how to use
```
 $ python robjc.py [TARGET DIR] [DESTINATION DIR (relative or absolute, default = same dir ./)] [CLASS NAME(default = 'R')]
```
It generates
```
R.h
R.m
```

and then, You can use it like below after import.
```objective-c
R.image_name
```

# TODO
* Integration with [Termini](https://github.com/metasmile/termini)
* Automatically import Xcode project with asset files
