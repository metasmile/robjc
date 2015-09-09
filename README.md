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

### Make a symbolic alias
This feature is very useful when you assign the uses of each image to the physical file which contains same content.
```
use_for_caseA.svg
use_for_caseB.svg
blabla.svg
```

BUT 3 files are perfectly same image... Perhaps you want to use a single file.

In that case, change the file name, as shown below.

```
use_for_caseA=use_for_caseB=blabla.svg
```

result :
```objective-c
+ (NSString *)use_for_caseA; {
    return @"use_for_caseA=use_for_caseB=blabla.svg";
}

+ (NSString *)use_for_caseB; {
    return @"use_for_caseA=use_for_caseB=blabla.svg";
}

+ (NSString *)blabla; {
    return @"use_for_caseA=use_for_caseB=blabla.svg";
}

```

so you can use like below
```
R.use_for_caseA
R.use_for_caseB
R.blabla
```

# TODO
* [ ] Support version of Swift
* [ ] Integration with [Termini](https://github.com/metasmile/termini)
* [ ] Automatically import Xcode project with asset files
* [x] Support symbolic alias [(1) file - (n) method]
* [ ] Support Xcode's i18n policy
* [ ] Generate a util category for taking UIImage or SVGKImage.
```ex) R.image_name.image / [[R.image_name] imageAsSVG:(CGSize)size]```
