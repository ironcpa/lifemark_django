function getAllSelectors() { 
    var ret = [];
    for(var i = 0; i < document.styleSheets.length; i++) {
        var rules = document.styleSheets[i].rules || document.styleSheets[i].cssRules;
        for(var x in rules) {
            if(typeof rules[x].selectorText == 'string') ret.push(rules[x].selectorText);
        }
    }
    return ret;
}


function selectorExists(selector) { 
    var selectors = getAllSelectors();
    for(var i = 0; i < selectors.length; i++) {
        if(selectors[i] == selector) return true;
    }
    return false;
}
