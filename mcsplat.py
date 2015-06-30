#import modules
from mcpi.minecraft import Minecraft
from mcpi import block
from time import sleep, time
from random import getrandbits

TEAMCOLS = [13,14]

def buildPitch(mc, pos):
    #glass cube
    mc.setBlocks(pos.x - 5, pos.y - 1, pos.z - 10,
                 pos.x + 5, pos.y + 3, pos.z + 10,
                 block.GLASS.id)

    #hollow it out
    mc.setBlocks(pos.x - 4, pos.y, pos.z - 9,
                 pos.x + 4, pos.y + 3, pos.z + 9,
                 block.AIR.id)

    #add 2 walls down the middle
    mc.setBlocks(pos.x, pos.y, pos.z - 7,
                 pos.x, pos.y + 3, pos.z - 1,
                 block.GLASS.id)

    #add 2 walls down the middle
    mc.setBlocks(pos.x, pos.y, pos.z + 1,
                 pos.x, pos.y + 3, pos.z + 7,
                 block.GLASS.id)

def splatBlock(mc, x, y, z, team):

    pointsScored = [0,0]

    #who is the other team
    otherTeam = 1 - team
    
    #what type of block has been hit
    blockHit = mc.getBlockWithData(x, y, z)
    #has a glass block been hit?
    if blockHit.id == block.GLASS.id:
        #claim it for the team
        mc.setBlock(x, y, z, block.WOOL.id, TEAMCOLS[team])
        #increase the teams score
        pointsScored[team] += 1
        
    #was it a wool block
    elif blockHit.id == block.WOOL.id:
        #if its the other teams colour turn it back to GLASS
        if blockHit.data == TEAMCOLS[otherTeam]:
            mc.setBlock(x, y, z, block.GLASS.id)
            #reduce the other teams score
            pointsScored[otherTeam] -= 1
        
    return pointsScored
            
#setup points
points = [0,0]

#create connection to Minecraft
mc = Minecraft.create()

#post the message to the screen
mc.postToChat("Minecraft Splat")

#find out the host players position
pos = mc.player.getTilePos()

#build the pitch
buildPitch(mc, pos)

sleep(3)

mc.postToChat("Go!")

#get a list of the players
players = mc.getPlayerEntityIds()

start = time()

gameOver = False
#continue till the end of the game
while not gameOver:

    #has a block been hit?
    blockHits = mc.events.pollBlockHits()
    for hit in blockHits:
        
        #which team was it
        team = players.index(hit.entityId) % 2
        
        pointsScored = splatBlock(
            mc, hit.pos.x, hit.pos.y, hit.pos.z, team)
        
        #update the points
        points[0] += pointsScored[0]
        points[1] += pointsScored[1]

        #splat blocks around it
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if getrandbits(1) == 1:
                        pointsScored = splatBlock(mc,
                                                  hit.pos.x + x,
                                                  hit.pos.y + y,
                                                  hit.pos.z + z,
                                                  team)
                        
                        #update the points
                        points[0] += pointsScored[0]
                        points[1] += pointsScored[1]
        
    #if the time has run out, set game over
    if time() - start > 30:
        gameOver = True
        mc.postToChat("Game Over")
        mc.postToChat("Green Team = " + str(points[0])) 
        mc.postToChat("Red Team = " + str(points[1]))          
        if points[0] > points[1]:
            mc.postToChat("Green Team wins")
        else:
            mc.postToChat("Red Team wins")
