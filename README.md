# Folder-Synchronizer
A program for one way synchronization between source and destination folder. What's in the source folder will be copied to the destination folder. What's not in the source folder, but present in the destination folder, will be removed.

# How to run (example)
```
python FolderSynchronizer.py -s "/Users/anilcharles/Downloads/work/source" -d "/Users/anilcharles/Downloads/work/destination" -i 3  -l '/Users/anilcharles/Downloads/work/log.txt'
```

# Args
```
-s, --source, provide the source folder directory
                        
-d, --destination, provide the destination folder directory
                      
-i, --interval provide the synchronization interval in seconds
                        
-l, --log,  add logs to file specified
```
