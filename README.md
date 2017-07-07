# python_agent

This is an attempt to write a basic python agent.

Authors: Vinai Rachakonda and Ziyang Wang

Running ast rewrite_code:
First delete all pyc files
```
find <path> -name \*.pyc -delete
```
Compile pyc:
```
python <path_to_rewrite_code.py> <path_to_application>
```
Then run the app

# Graphing

If you want to quickly see a graph of memory usage or time per request run the following

```
python <path_to_analysis/grapher.py> ./times.log
```
or
```
python <path_to_analysis/grapher.py> ./memory_profiler.log
```