# R_objc
Simple objective-c resource class generator inspired by android.R.

## usage
```
$ robjc ~/Documents/myproj/resources
```
```
usage: robjc.py [-h] [-c [CLASS_NAME]] [-m [MAP_DIR_STRUCTURE]]
                [-a [ALIAS_ENABLED]] [-l [SHOW_LOG]]
                [<target path>] [<destination path>]

Objective-c resource class generator

positional arguments:
  <target path>         Target path to read directories. (default=./)
  <destination path>    Destination path to create a class file. (default=./)

optional arguments:
  -h, --help            show this help message and exit
  -c [CLASS_NAME], --class-name [CLASS_NAME]
                        Class name. (default=R)
  -m [MAP_DIR_STRUCTURE], --map-dir-structure [MAP_DIR_STRUCTURE]
                        Map structure of all directories from target path.
                        (default=False)
  -a [ALIAS_ENABLED], --alias-enabled [ALIAS_ENABLED]
                        Enabling symbolic alias. (default=False)
  -l [SHOW_LOG], --show-log [SHOW_LOG]
                        Show log. (default=False)
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

### Mapping dir structure
You can write same directory structure via target path.
```
/Users/user/Documents/myproj/resources/image1.png
~/Documents/myproj/resources/image2.png
~/Documents/myproj/resources/sounds/sound1.caf
~/Documents/myproj/resources/sounds/sound2.caf
~/Documents/myproj/resources/sounds/ui/sound3.caf
```
add a option '-m'.
```
$ robjc -m ~/Documents/myproj/resources
```

result:
```objective-c
R.image1
R.image2
R.sounds.sound1
R.sounds.sound2
R.sounds.ui.sound3
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
add a option '-a'.
```
$ robjc -a ~/Documents/myproj/resources
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
* ```ex) R.image_name.image / [[R.image_name] imageAsSVG:(CGSize)size]```
* [x] Support DIR structure mapping
