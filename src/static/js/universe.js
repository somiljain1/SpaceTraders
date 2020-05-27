var universe = JSON.parse(universe);
var regionList = document.getElementById("RegionList");
var currentRegionName = document.getElementById("CurrentRegionName");
var currentRegionCoords = document.getElementById("CurrentRegionCoords");
var currentRegionTechLevel = document.getElementById("CurrentRegionTechLevel");
    
console.log(universe);
console.log(universe[0].Coordinates);

function travelToRegion() {
    var nextRegion = universe[regionList.selectedIndex];
    console.log(nextRegion);
    currentRegionName.innerHTML = "Region Name: " + nextRegion.Name;
    currentRegionCoords.innerHTML = "Region Coordinates: (" + nextRegion.Coordinates + ")";  
    currentRegionTechLevel.innerHTML = "Region Tech Level: " + nextRegion.TechLevel;

    for (i = 0; i < regionList.options.length; i++) {
            updateRegionList(nextRegion, universe[i], i)
    }
}

function updateRegionList(nextRegion, region, index) {
    var newDistance = calcDistance(nextRegion.Coordinates, region.Coordinates)
    var sub = regionList.options[index].text.split(")")[0]
    sub += ") Distance: " + newDistance
    regionList.options[index].text = sub
}

function calcDistance(region1, region2) {
    var r1x = region1.split(", ")[0] 
    var r1y = region1.split(", ")[1]
    var r2x = region2.split(", ")[0] 
    var r2y = region2.split(", ")[1]  
    var distance = Math.round(Math.pow(Math.pow(r1x - r2x, 2) + Math.pow(r1y - r2y, 2), 1/2))
    return distance;
}

//called on page startup
function init(){
    //load items into the dropdown
    var index = Math.floor(Math.random() * 10);
    var selectedRegion = universe[index];
    currentRegionName.innerHTML = "Region Name: " + selectedRegion.Name;
    currentRegionCoords.innerHTML = "Region Coordinates: (" + selectedRegion.Coordinates + ")";  
    currentRegionTechLevel.innerHTML = "Region Tech Level: " + selectedRegion.TechLevel; 

    universe.forEach(initRegionList)
    function initRegionList(item) {
        var region = document.createElement("option")
        var distance = calcDistance(selectedRegion.Coordinates, item.Coordinates)
        region.text = item.Name + "(" + item.Coordinates + ")" + " Distance: " + distance
        regionList.add(region)
    }
}