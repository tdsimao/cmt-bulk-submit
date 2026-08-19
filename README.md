

### instructions

1. indicate the `conference` in the file `config.json`, this can be find in the submission url: https://cmt3.research.microsoft.com/<conference>/Track/1/Submission/Create
1. provide the list of papers in the file `papers.json`. Note that some tracks have restrictions in the number of files, so the list of files might have a single item.
	- title
	- abstract
	- files: paths to the files to be submited
	- trackID: id of the track
1. install the necessary dependencies 

```bash
uv sync
```

1. run the script
```bash
uv run cmt-submit
```

