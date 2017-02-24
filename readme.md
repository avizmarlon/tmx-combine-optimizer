### What is it for?

This is for people (mostly translators) that need to combine multiple TMX files into one large TMX file, but in order to do that, all TMX files must have the same srclang value. But checking 3000+ .tmx files by hand is just too boring. This script will do the hard work.

### What does it do?

This script looks for all .tmx files in set of folders and subfolders and analyze all of them to find the srclang attribute of the header tag.

Then it will check if all srclang values are consistent with each other.