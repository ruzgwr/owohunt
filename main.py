import multiprocessing
import etc.graphics.consolegraphics 
import etc.configreader
import importlib
import time
try:
  import etc.graphics.windowgraphics
  graphics = etc.graphics.windowgraphics.window()
  GUI=True
except:
  GUI=False

cheats = []
graphics.profile_selector()
profile = graphics.returnlast()
profile=etc.configreader.profile(profile_name=profile)
print(profile)
runwindow = graphics.runningwindow(profile)
    
cheats = etc.configreader.cheats(profile)
i = 0
for cheat in cheats:
  #import module
  try:
    cheats[i][0] = importlib.import_module(cheat[0])
    graphics.register_engine(cheats[i][0], ("off" if cheat[1] == False else "running"))
  except:
    class failed_module:
      name=cheats[i][0]
    graphics.register_engine(failed_module, "alarm")
  i+=1
while True:
  graphics.update()