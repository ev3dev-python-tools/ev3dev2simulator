
  update ev3dev2simulator pyproject.toml with fixes
   => test them on mac/linux with my own testpypi!
   mac/windows wheels upload to pypi  
   


===================================================================================================================
fixes at 2024-05-19 on ev3dev2simulator v2.0.6  so works again on all platforms with python 3.12
 -> ev3dev2simulator v2.0.7 release
===================================================================================================================
 


problems with installing ev3dev2simulator v2.0.6 (released 2022 dec)
================================================

-> we found problems with installling  ev3dev2simulator
   on python 3.8 - python 3.21
   for macos/windows/linux
  
   
 -> the following packages had  problems:
       * simpleaudio 
           -> see simpleaudio.txt
           
              problems found: 
                1) simpleaudio broken on python 3.12 in general(for all platforms)
                2) no wheels available for simpleaudio on macos/windows making install cumbersome because need c-compiler 
              
             solutions found:
               1) patch from  https://github.com/cexen/py-simple-audio  solves problem with python 3.12
               2) build wheels for simpleaudio on macos/windows in my own project
                    https://github.com/harcokuppens/py-simple-audio/
                 which is renamed to simpleaudio_patch to have a place on pypi for the wheels
             
             thus solution is
                forked project 'simpleaudio_patch' in https://github.com/harcokuppens/py-simple-audio/
                in which patches are applied for python3.12 and wheels are build 
                for macos/windows with github actions workflow 
                   https://github.com/harcokuppens/py-simple-audio/blob/master/.github/workflows/wheels.yml
                adjust the requirements to: 
                  "simpleaudio_patch" 
                note: for linux no wheels are build for simpleaudio because problems with manylinux wheel on ubuntu
                
              
       * pyttsx3 
           -> see pyttsx3.txt
           
              problems found: 
                1) pyttsx3 build broken on macos sonoma
                   -> seems that the c library of the macos system has changed,
                      and that therefore c-call to a system library by pyttsx3 fails!!
                2) py3-tts fixes pyttsx3 on macos, but still breaks on python 3.12
       
        
              solutions found:
                1) do not use pyobjc==10 , but switch to  pyobjc==9.0.1 
                   do this by switching to 
                      pyttsx3 -> py3-tts (requires pyobjc==9.0.1)
                   note: the current latest pyobjc version is v10.1 (maybe later versions will work again??)    
           
                2) for mac:  pyobjc==9.0.1    ->  pyobjc==9.2  
                     then no problems on python 3.12
           
              thus the solution is simply to just adjust the requirements to: 
                "py3-tts" 
                "pyobjc==9.2; platform_system == 'Darwin'"
                        
                       
   note: python 3.12 was released on  October 2, 2023
         pyobjc==10  released on Dec 9, 2023 
         
          -> later then ev3dev2simulator v2.0.6 (released 2022 dec)    
              so could never be tested on python 3.12 with  pyobjc==10 at dec. 2022
              so not strange problems happen there
              


Changes to ev3dev2simulator requirements
=========================================


requirements  ev3dev2simulator v2.0.6    
--------------------------------------
          
    https://github.com/ev3dev-python-tools/ev3dev2simulator/blob/v2.0.6/setup.py
      'ev3devlogging', 
      'arcade==2.6.16', 
      'pypiwin32; platform_system=="Windows"',
      'pyobjc;sys.platform=="darwin"', 
      'simpleaudio==1.0.4', 
      'pyttsx3==2.7', 
      'numpy', 
      'strictyaml'],

    
     -> currently only works on windows with python 3.8, (binary wheels available)
        also works on mac/linux for python 3.8 and 3.10 but need to build wheels yourself
     -> not working on python 3.12 
     
     
requirements  ev3dev2simulator v2.0.7  
--------------------------------------            

   -> works on mac/windows till python 3.12 (binary wheels available)
   -> also works on linux till python 3.12 but need to build wheels yourself,
      which wouldn't normally be a problem on linux, but you need to install
      some dev-packages first to make the build work. (see linux requirements below)
      

 https://github.com/ev3dev-python-tools/ev3dev2simulator/blob/main/pyproject.toml

    'ev3devlogging',
    'arcade==2.6.16',
    'simpleaudio_patch',
    # simpleaudio patched and wheels available for mac/windows till python 3.12
    'py3-tts',
    # py3-tts improves older pyttsx3 and requires in its deps:
    #  "comtypes; platform_system == 'Windows'",
    #  "pypiwin32; platform_system == 'Windows'",
    #  "pywin32; platform_system == 'Windows'",
    #  "pyobjc==9.0.1; platform_system == 'Darwin'",
    # for python3.12 on darwin 9.0.1 we get error, fix:
    "pyobjc==9.2; platform_system == 'Darwin'",
    'numpy',
    'strictyaml',
    # need python 3.8 and pylint < 2.6 because otherwise
    # problems linting https://github.com/pylint-dev/pylint/issues/6813 no-space-check was removed in 2.6
    # other problems causing python 3.8 : https://github.com/zylon-ai/private-gpt/issues/884  https://github.com/pylint-dev/pylint/issues/3882
    'pylint==2.5.3'

     


 extra requirements for linux users:
 
           The pyttsx3  python speech library  uses system libraries in its implementation.
           For mac/windows the used system 'speak' libraries are always available,
           but for linux you must sure these are installed with:
            
              sudo apt update && sudo apt install espeak ffmpeg libespeak1
      
          For linux there are is no binary distribution available for simpleaudio.
          The Python 3 and ALSA development packages are required for pip to build the extension. 
          For Debian variants (including Raspbian), this will usually get the job done:
                           
                sudo apt-get install -y python3-dev libasound2-dev







         
                                                                
              
              

