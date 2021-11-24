# How to submit lardon jobs on `lxplus`

- You *cannot* submit condor jobs from `eos`, only from `afs`.
- In your `afs` repository, symbolic links to all the code from `eos` works
- The code needs absolute paths everywhere to work on condor

- In runs.txt, list all the files you want to reconstruct
- Put your correct path in `script.sh` and `submit.sub`

To submit jobs : `condor_submit submit.sub`
To monitor jobs : `condor_q`
To know more about condor and lxplus : 
<https://batchdocs.web.cern.ch/index.html>
