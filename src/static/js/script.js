var skillPoints;
var difficulty = document.getElementsByName("difficulty");

    function recalcSP() {
        for (i = 0; i < difficulty.length; i++) {
            if (difficulty[i].checked) {
                document.getElementById('selectedDifficulty').value = document.getElementsByName("difficulty")[i].value;
                console.log(document.getElementById('selectedDifficulty').value)
                skillPoints = 4 * (4 - i);
            }
        }
        document.getElementById("skillPointCounter").innerHTML = "Skill Points: " + skillPoints;
        return skillPoints;
    }

    function validateInput() {
        var skillPoints = recalcSP();
        var pilotskills =  parseInt(document.getElementById('pilotskills').value);
        var fighterskills = parseInt(document.getElementById('fighterskills').value);
        var merchantskills = parseInt(document.getElementById('merchantskills').value);
        var engineerskills = parseInt(document.getElementById('engineerskills').value);
        var pointsAllocated = pilotskills + fighterskills + merchantskills + engineerskills;

        if (document.getElementById("name").value === '') {
            alert('Error: Please enter a name for the player');
            return false;
        }
        //console.log(pilotskills + fighterskills);
        if (pointsAllocated > skillPoints || pilotskills < 0 || fighterskills < 0 
                || merchantskills < 0 || engineerskills < 0) {
            alert('Error: Exceeded skill points or negative points allocated');
            return false;
        } else {
            if (pointsAllocated < skillPoints) {
                var result = confirm("You have not allocated all of your skill points. Do you still want to proceed?");
                if (result === false) {
                    return false;
                }
            }
            return true;
        }
    }