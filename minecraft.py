import mcpi.minecraft
import time
import random

mc = mcpi.minecraft.Minecraft.create()

mc.postToChat("Hello Minecraft World")


# this command makes the program run over and over again in a "loop"
while 1:


    # the "raw_input" command lets the user type in a command
    command = raw_input('Command: ')


    if command == "teleport":

        x = random.randint(-100, 100)
        y = 20
        z = random.randint(-100, 100)
        mc.postToChat("Teleporting to x: " + str(x) + " z: " + str(z))
        mc.player.setTilePos(x, y, z)


    if command == "cube":

        x = mc.player.getPos().x + 1
        y = mc.player.getPos().y
        z = mc.player.getPos().z + 1
        length = 4
        width = 5
        height = 3
        outsideblocktype = 56
        insideblocktype = 0

        mc.setBlocks(x, y, z, x+length, y+height, z+width, outsideblocktype)       
        mc.setBlocks(x+1, y, z+1, x+length-1, y+height-1, z+width-1, insideblocktype)       

        
    if command == "pyramid":

        x = mc.player.getPos().x + 1
        y = mc.player.getPos().y
        z = mc.player.getPos().z + 1
        width = 8
        blocktype = 56

        for side in range(width, -1, -2):
            mc.setBlocks(x, y, z, x+side, 0, z+side, blocktype)
            x = x+1
            y = y+1
            z = z+1

        
    if command == "pattern":

        x = mc.player.getPos().x + 1
        y = mc.player.getPos().y
        z = mc.player.getPos().z + 1

        blocks = [[1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 2, 2, 2, 2, 2, 2, 2]]

        for row in reversed(blocks):
            for block in row:
                mc.setBlock(x, y, z, block)
                x = x+1
            y = y+1
            x = mc.player.getPos().x + 1


    if command == "quit":
        break
