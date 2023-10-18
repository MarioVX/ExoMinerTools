# ExoMinerTools
Some helper scripts for the game ExoMiner by ExoCorp

## RC Optimizer & Planetary Scheduler
###Description
This tool helps with the Refine and Construct quests of your current planetary. It is best suited for use in higher planetaries, as some of its assumptions are poorly applicable to the early game.
When executed, it prompts user input on the user's current Refinery & Constructor slots & level and rank. Based on this, it computes and reports:
1. Possible time saving on the current planetary from unlocking another Refinery or Constructor slot respectively. This can help decide whether farming more cash at the beginning of a planetary is worth it.
2. Which speed level to upgrade next for the greater total planetary time saving.
3. An optimal schedule for the current planetary with current settings. Lists for each rank the time it takes to complete, the portion of that time your refineries and constructors need to spend producing each recipe, and the target final stock of the product.

###Dependencies
- numpy
- scipy.optimize

###Assumptions
- You complete all refinery and constructor related research at the very beginning of the planetary, before you start tackling the rank quests. This is not recommended on early planetaries, but due to the rank quests' quotas always increasing but research requirements staying the same, the higher your planetary the better this assumptions matches perfect play.
- Refinery and constructor slots remain constant throughout the planetary. Use the first output to gauge for how long cash farming for the next slot is still worth it, then run with the final slot counts once it no longer is.
- There are always sufficient raw materials in your mothership to run any refinery recipe unhindered. Maintain sufficient supply by upgrading your deposits.
- Any time required for any other type of quest other than Refine or Construct is neglected. Make sure you're appropriately stockpiling the resources for big Collect quests at some deposits to avoid wasting time here. If you can't stockpile enough resources in time you should invest some relics into crates and astronauts rather than upgrading refine and construct speeds further. This tool cannot account for this. If the next rank (as recognized by this tool) includes producing ingredients rather than exclusively the item that is subject to the Refine / Construct quest, you can bridge some collecting time by producing these ingredients first and saving the target item for when the rank in question is actually reached.
- Items are modeled as continuous quantities, not discrete ones. Similarly, slots are not discretely represented. The tool may propose a fractional production that can't be precisely replicated in game. For increasingly higher planetaries, the caused discrepancy gets negligible.
- Specialist researches (10% chance to create double) are accounted for by having the recipes produce 1.1 products per cycle without increased ingredient demand. This matches the real behavior in the long term, i.e. increasingly better for larger quantities. For example, to produce 1000 Cables this tool internally assumes you need 1000/1.1 * 4 = 3,636.36... Refined Carbon. The output will round these up to the next whole number. It should still be kept in mind that individual results will be subject to random variance, so in the case of ingredients you might want to produce a couple extra to not be caught off guard by being a few items short to complete the rank, and having to repeat a whole cycle. The extra amount you need to ensure some % chance of being sufficient to produce the target quota is expected to grow by the square root of the quota. That means it slowly grows in absolute terms but shrinks in % of the total quota the bigger the latter gets.
