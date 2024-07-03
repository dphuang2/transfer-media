exiftool -r -P -o .
'-FileName<$FileModifyDate/${FileModifyDate#;DateFmt("%Y-%m-%d_%H%M%S")}_%f%-c.%e'
'-FileName<$DateTimeOriginal/${DateTimeOriginal#;DateFmt("%Y-%m-%d_%H%M%S")}_%f%-c.%e'
'-FileName<$FileModifyDate/${model;}/${FileModifyDate#;DateFmt("%Y-%m-%d_%H%M%S")}_${model}_%f%-c.%e'
'-FileName<$DateTimeOriginal/${model;}/${DateTimeOriginal#;DateFmt("%Y-%m-%d_%H%M%S")}_${model}_%f%-c.%e'
-d '/Volumes/Documents/DestinationDrivePath/%Y/%m/%d' /Volumes/SourceDrivePath