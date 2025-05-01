Usage: reaper [options] [projectfile.rpp | mediafile.wav | scriptfile.lua [...]]

Multiple media files and/or scripts may be specified, and will be added or run in order.
-nonewinst can be used to add media files and/or run scripts in an already-running instance of REAPER.

Options:
  -audiocfg : show audio configuration at startup
  -cfgfile file.ini : use full path for alternate resource directory, otherwise uses default path
  -new : start with new project
  -template filename.rpp : start with template project
  -saveas newfilename.rpp : save project (after creating/loading) as file
  -renderproject filename.rpp : render project and exit
  -ignoreerrors : do not show errors on load
  -nosplash : do not show splash screen window
  -splashlog /path/to/filename.log : write splash screen message log to file
  -newinst | -nonewinst : override preference for new instance checking
  -close[all][:save|:nosave][:exit] : close project(s), optionally not prompting for save and exiting
  -noactivate : control but do not activate existing instance
  -batchconvert filelist.txt : batch converter mode, filelist.txt contains (#=comments):
     filename.wav
        # or
     filename.wav(TAB CHARACTER)outputfile.wav
        # plus any number of additional files
     <CONFIG    # optional block NOTE: can be generated via the Batch Converter presets button
       SRATE 44100      # omit to use source sample rate
       NCH 2    # omit to use source channel count
       RSMODE modeidx   # resample mode, copy from project file
       DITHER 3         # 1=dither, 2=noise shaping, 3=both
       USESRCSTART 1    # 1=write source media BWF start offset to output
       USESRCMETADATA 1         # 1=attempt to preserve original media file metadata if possible
       TRIM_START 0.0   # trim leading silence, 0.5=-6dB peak
       TRIM_END 0.0     # trim trailing silence, 0.5=-6dB peak
       PAD_START 0.0    # leading silence, 0.001=1ms, can be negative
       PAD_END 0.0      # trailing silence, 0.001=1ms, can be negative
       OUTPATH 'path'
       OUTPATTERN 'wildcardpattern'
       NORMALIZE 1 -6.0 0       # 1st parameter: 1=peak, 2=true peak, 3=lufs-i, 4=lufs-s, 5=lufs-m
                                # 2nd parameter: dB target, 3rd parameter: 1=normalize only if too loud
       BRICKWALL 1 -1.0         # 1=peak, 2=true peak, 2nd parameter: dB ceiling
       FADE 0.0 0.0 1 1         # fade-in length (0.001=1ms), fade-out length, fade-in shape, fade-out shape
       FXCHAIN 'fxchainfilename'        # use full path if specified, otherwise FxChains directory
       FX_NCH 4         # default 4 channels for FX processing
       CPULIMIT 0       # 0 or omit=use all available CPU cores, 1=limit to 1 core, etc
       <FXCHAIN
                # contents of .RfxChain file
       >
       <OUTFMT
                # base64 data, e.g. contents of <RENDER_CFG or <RECORD_CFG block from project file
       >
       <METADATA
                # contents of <RENDER_METADATA block from project file
       >
     >
