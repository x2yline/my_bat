
REM ÏÂÔØSRA£ºftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR539/SRR5396632/SRR5396632.sra
for %%i in (*.sra) do F:\ngs\sratoolkit.2.8.2-win64\sratoolkit.2.8.2-win64\bin\fastq-dump.exe --split-3 %%i