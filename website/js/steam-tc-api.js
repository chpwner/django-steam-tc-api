//some awesome prototypes
//super awesome numerical hash, no really a lifesaver!
String.prototype.hashCode = function () {
    var hash = 0,
        i, char;
    if (this.length == 0) return hash;
    for (i = 0, l = this.length; i < l; i++) {
        char = this.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
};
//repeatables
String.prototype.repeat = function (num) {
    var cat = '';
    var dog = this;
    for (var i = 0; i < num; i++) {
        cat = cat + dog;
    }
    return cat;
}

function getCookie(c_name)
{
var c_value = document.cookie;
var c_start = c_value.indexOf(" " + c_name + "=");
if (c_start == -1)
  {
  c_start = c_value.indexOf(c_name + "=");
  }
if (c_start == -1)
  {
  c_value = null;
  }
else
  {
  c_start = c_value.indexOf("=", c_start) + 1;
  var c_end = c_value.indexOf(";", c_start);
  if (c_end == -1)
  {
c_end = c_value.length;
}
c_value = unescape(c_value.substring(c_start,c_end));
}
return c_value;
}

function setCookie(c_name,value,exdays)
{
var exdate=new Date();
exdate.setDate(exdate.getDate() + exdays);
var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
document.cookie=c_name + "=" + c_value;
}

$( document ).ready(function() {
    var cookie = getCookie('chpwner');
    if (cookie == 1){
        loader();
        setCookie('chpwner',0,1);
    }
});

function loader() {
    $('#error').empty();
    $('#playerName').html('<h1>Viewing All Games</h1>');
    var opts = {
        lines: 13,
        // The number of lines to draw
        length: 20,
        // The length of each line
        width: 10,
        // The line thickness
        radius: 30,
        // The radius of the inner circle
        corners: 1,
        // Corner roundness (0..1)
        rotate: 0,
        // The rotation offset
        direction: 1,
        // 1: clockwise, -1: counterclockwise
        color: '#000',
        // #rgb or #rrggbb or array of colors
        speed: 1,
        // Rounds per second
        trail: 60,
        // Afterglow percentage
        shadow: false,
        // Whether to render a shadow
        hwaccel: false,
        // Whether to use hardware acceleration
        className: 'spinner',
        // The CSS class to assign to the spinner
        zIndex: 2e9,
        // The z-index (defaults to 2000000000)
        top: '30',
        // Top position relative to parent in px
        left: 'auto' // Left position relative to parent in px
    }
    var target = document.getElementById('stage');
    var spinner = new Spinner(opts).spin(target);
    webstuff(spinner, function (spinner) {
        spinner.stop();
    });
}
//globalstore
var store = {};

function webstuff(spinner, callback) {
    $.getJSON('https://api.chpwner.org/data/Games/', function (games) {
        var length = games.length;
        var c = 0;
        var ctotal = 0;
        for (var i = 0; i < length; i++) {
            var jd = games[i];
            //console.log(jd);
            jd.idhash = 'g' + jd.name.hashCode();
            store[jd.idhash] = jd;
            jd.sum = 0;
            jd.fsum = 0;
            jd.count = 0;
            jd.fcount = 0;
            jd.time = 0;
            for (var j in jd.cards) {
                var jsonstring = jd.cards[j];
                //console.log(jsonstring);
                var parse = JSON.parse(jsonstring);
                var time = "";
                if (parse.trading_card == true && parse.itemtype.indexOf("Foil") == -1) {
                    //override cards with price to get array of prices of cards
                    //jd.cards[j] = parse.price;
                    jd.time = parse.updated;
                    jd.sum = jd.sum + parse.price;
                    jd.count++;
                } else if (parse.trading_card == true && parse.itemtype.indexOf("Foil") != -1) {
                    //override cards with price to get array of prices of cards
                    //jd.cards[j] = "foil "+ parse.price;
                    jd.time = parse.updated;
                    jd.fsum = jd.fsum + parse.price;
                    jd.fcount++;
                } else {
                    //override cards with price to get array of prices of cards
                    //jd.cards[j] = "not a card";
                    //jd.time = parse.updated;
                }
            }
            jd.avg = (jd.sum / jd.count).toFixed(2);
            jd.favg = (jd.fsum / jd.fcount).toFixed(2);
            jd.ccs = (jd.count * jd.avg).toFixed(2);
            jd.ccfs = (jd.fcount * jd.favg).toFixed(2);
            if (jd.count > 0) {
                if (jd.count != jd.fcount) {
                    flag = ' error';
                } else {
                    flag = '';
                }
                $('#stage').append('<tr id="' + jd.idhash + '" class="cardrow' + flag + '"><td class="jdname">' + jd.name + '</td><td class="jdcount">' + jd.count + '/' + jd.fcount + '</td><td class="cardsowned">0</td><td class="fcardsowned">0</td><td class="percentage">0%</td><td class="lvl">0</td><td class="flvl">0</td><td class="jdavg">' + jd.avg + '</td><td class="jdfavg">' + jd.favg + '</td><td class="ccs">' + jd.ccs + '</td><td class="ccfs">' + jd.ccfs + '</td><td class="jdtime">' + jd.time + '</td><td><button type="button" class="btn btn-small upbtn" name="update" value="' + jd.name + '" id="' + jd.idhash + '" data-loading-text="Loading...">update</button></td><\/tr>');
                c++;
                ctotal = ctotal + jd.count + jd.fcount;
            } else {
                $('#stage').append('<tr id="' + jd.idhash + '" class="noncardrow"><td class="jdname">' + jd.name + '</td><td class="jdcount">0</td><td class="cardsowned">0</td><td class="fcardsowned">0</td><td class="percentage">0%</td><td class="lvl">0</td><td class="flvl">0</td><td class="jdavg">0</td><td class="jdfavg">0</td><td class="ccs">0</td><td class="ccfs">0</td><td class="jdtime">0</td><td><button type="button" class="btn btn-small upbtn" name="update" value="' + jd.name + '" id="' + jd.idhash + '" data-loading-text="Loading...">update</button></td><\/tr>');
            }
        }
        //table sorter
        $("#datatable").tablesorter();
        //spinner stopper callback
        callback(spinner);
        //some jquery setup
        $('#searchBtn').attr('disabled', false);
        $('#gamecount').text('Game Count: ' + length);
        $('#itemcount').text('Card Count: ' + ctotal);
        $('#badgecount').text('Badge Count: ' + c * 2);
        //load buttons
        buttons();
    }).fail(function (jqxhr, textStatus, error) {
        spinner.stop();
        var err = textStatus + ', ' + error;
        $('#error').append('Request Failed ' + err);
    })
}

function validateID(InString) {
    if (InString.length != 17) return (false);
    var RefString = "1234567890";
    for (Count = 0; Count < InString.length; Count++) {
        TempChar = InString.substring(Count, Count + 1);
        if (RefString.indexOf(TempChar, 0) == -1)
            return (false);
    }
    return (true);
}
//globals?
var tr;
var p;
var pstore = {};

function getUser(form) {
    //disable some buttons
    $('#sub').attr('disabled', true);
    //hide progress bar
    $('#infobar').attr('style', 'display:none');

    //reset hide if applicable
    if (p) {
        $('#toggle').trigger('click');
    }

    //reset flags
    $('#stage').children('tr.flag').removeClass('flag');
    //reset filtered games if applicable
    $('#stage').append(tr);

    var steamid = form.steamid.value;
    form.steamid.value = "Loading...";
    form.searchBtn.disabled = true;

    if (validateID(steamid)) {
        data = {
            'steamid': steamid
        };
    } else if (steamid != '') {
        data = {
            'personaname': steamid
        };
    } else {
        //reenable buttons
        form.searchBtn.disabled = false;
        form.steamid.value = "No ID entered!";

        return ('no id entered');
    }
    $.getJSON('https://api.chpwner.org/data/Players/', data, function (profile) {
        var profile = profile[0];
        if (!(profile)) {
            //reset pstore
            pstore = {}
            //reenable buttons
            $('#sub').attr('disabled', false);
            form.searchBtn.disabled = false;
            form.steamid.value = "Not Found!";
            $('#gamecount').html('<span style="color:red">Hint: use the "Update Profile" button to add a new ID</span>');
            return ('user not in database');
        }
        pstore = profile;
        form.searchBtn.disabled = false;
        form.steamid.value = "Finished!";
        $('#playerImage').attr('src', profile.avatar);
        $('#playerName').html("<h1>Viewing " + profile.personaname + "'s Games</h1>");
        $('#gamecount').text('Game Count: ' + profile.licenses.length);
        $('#itemcount').html('Item Count: <a href="#invModal" onClick="modal()">' + profile.items.length + '</a>');
        $('#badgecount').text('Badge Count: ' + profile.badges.length);
        var lvlArr = [0, 0, 0, 0, 0, 0];
        var foil = 0;
        for (var i in profile.badges) {
            var badge = profile.badges[i];
            var pos = badge.indexOf('vl:');
            var lvl = badge.substring(pos + 3, pos + 4);
            if (badge.indexOf('Foil') == -1) {
                lvlArr[lvl]++;
            } else {
                foil++;
            }
        }
        $('#lvl1').text(lvlArr[1]);
        $('#lvl2').text(lvlArr[2]);
        $('#lvl3').text(lvlArr[3]);
        $('#lvl4').text(lvlArr[4]);
        $('#lvl5').text(lvlArr[5]);
        $('#lvlFoil').text(foil);

        //modify table
        var len = profile.personaname.length + 3;
        for (var j in profile.licenses) {
            var game = 'g' + profile.licenses[j].substring(len).hashCode();
            $('#' + game).addClass('flag');
            updateTable(game);
        }
        //remove nonflagged
        tr = $('#stage').children('tr:not(tr.flag)').detach();
        //update tablesorter
        $("#datatable").trigger("update");

        //reenable buttons
        $('#sub').attr('disabled', false);
    })
        .fail(function (jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.log("Request Failed: " + err);
            form.steamid.value = "Request Failed: " + err;
            form.searchBtn.disabled = false;
        })
    return (true);
}

function updateTable(id) {
    //reset notifiers
    $('#' + id).removeClass('success');
    $('#' + id).removeClass('info');
    $('#' + id).removeClass('warning');
    $('#' + id).children('td.percentage').attr('style', '')

    var jd = store[id];
    if (!(jd)){
        console.log("unloaded game detected, skipping");
        return(false);
    }
    
    var gamename = jd.name;
    var cards = {};
    var badgeObj = {};

    //check if profile data loaded and we have a game with cards
    if (pstore && jd.count > 0) {
        //manipulate items to get assoc array of hashcodes
        //for the most part json str are goning to be the same
        //unless an update was triggered after getting composite data
        //but before getting the profile
        var items = pstore.items;
        for (var i in items) {
            var jsonstring = items[i];
            var parse = JSON.parse(jsonstring);
            //skip nontrading cards
            if (!(parse.trading_card) && pstore.done == 1) {
                continue;
            }
            var idhash = 'hc' + parse.itemname.hashCode();
            if (cards[idhash]) {
                cards[idhash]['quanity']++;
            } else {
                cards[idhash] = {
                    'itemtype': parse.itemtype,
                    'itemname': parse.itemname,
                    'quanity': 1
                };
            }
        }
        
        if (pstore.done != 1){
        $("#plyInv").empty();
        $("#invModalLabel").text(pstore.personaname + "'s Inventory");
        for (var key in cards){
            var item = cards[key];
            $("#plyInv").append("<li><strong>" + item.itemname + "</strong> (" + item.quanity + ") <i>"+ item.itemtype + "</i></li>");
        }
        }
        pstore.done = 1;

        var owned = 0;
        var fowned = 0;
        for (var k in jd.cards) {
            var jsonstring = jd.cards[k];
            if (typeof (jsonstring) === "object") { //update script already did the conversion
                var parse = jsonstring;
            } else {
                var parse = JSON.parse(jsonstring);
            }
            //skip nontrading cards
            if (!(parse.trading_card)) {
                continue;
            }
            var hash = 'hc' + parse.itemname.hashCode();
            if (cards[hash] && parse.itemtype.indexOf('Foil') == -1) {
                owned++;
            } else if (cards[hash] && parse.itemtype.indexOf('Foil') != -1) {
                fowned++;
            }
        }
        $('#' + id).children('td.cardsowned').text(owned);
        $('#' + id).children('td.fcardsowned').text(fowned);

        var fraction = owned + '/' + jd.count;
        var percent = ((owned / jd.count) * 100).toFixed(0);
        var ps = percent + '% = ' + fraction
        $('#' + id).children('td.percentage').text(ps)
        if (percent >= 50) {
            $('#' + id).children('td.percentage').attr('style', 'color:green')
        }

        var ccs = ((jd.count - owned) * jd.avg).toFixed(2);
        $('#' + id).children('td.ccs').text(ccs);

        var ccfs = ((jd.fcount - fowned) * jd.favg).toFixed(2);
        $('#' + id).children('td.ccfs').text(ccfs);

        var badges = pstore.badges;
        for (var j in badges) {
            var badge = badges[j];
            var pos = badge.indexOf(' (Lvl:');
            var badgename = badge.substring(0, pos);
            var sets = badge.substring(pos + 6, pos + 7)
            var idhash = 'g' + badgename.hashCode();
            badgeObj[idhash] = sets;
        }
        if (badgeObj[id]) {
            str = badgeObj[id] + " :) ".repeat(badgeObj[id]);
            if (badgeObj[id] == 5) {
                str = "5 :D"
                $('#' + id).addClass('success');
                $('#' + id).children('td.percentage').text('100%')
                $('#' + id).children('td.ccs').text('Maxed!');
            } else if (badgeObj[id] == 4) {
                //$('#'+id).addClass('info');
            }
        } else {
            str = "0";
        }
        $('#' + id).children('td.lvl').text(str);

        var fid = 'g' + (gamename + ' (Foil)').hashCode();
        if (badgeObj[fid]) {
            str = "1 XD";
            $('#' + id).children('td.ccfs').text('Maxed!');
            $('#' + id).addClass('success');
            if (badgeObj[id] == 5) {
                $('#' + id).removeClass('success');
                $('#' + id).addClass('warning');
                $('#' + id).children('td.percentage').text('200%')
                $('#' + id).children('td.lvl').text('6 ;)');
            }
        } else {
            str = "0";
        }
        $('#' + id).children('td.flvl').text(str);
    }
}

function buttons() {
    //game info trigger
    $('#stage').children().click(function () {
        gameLookup(this);
        location.href = "#top";
    });

    //price update button
    $('.upbtn')
        .click(function () {
            var btn = $(this);
            btn.button('loading');
            updatePrice(btn, function (btn) {
                btn.button('reset');
            });
        })

    //hide button
    //var p; is global now
    $("#toggle").click(function () {
        if (p) {
            console.log("unclicked");
            p.appendTo("#stage");
            p = null;
            $("#datatable").trigger("update");
            $("#toggle").text('Hide Noncard Games');
        } else {
            console.log("clicked");
            p = $("tr.noncardrow").detach();
            $("#datatable").trigger("update");
            $("#toggle").text('Show Noncard Games');
        }
    });
}
//disable enter key so user has to click buttons
$(document).keypress(
    function (event) {
        if (event.which == '13') {
            event.preventDefault();
        }
    });

function gameLookup(self) {
    var id = $(self).attr('id');
    var jd = store[id];
    var gamename = jd.name;
    var cards = {};
    var badgeObj = {};

    //clear old data
    $('#gameinfo').find('tr').empty();
    //write title
    $('#gametitle').text(gamename);

    //check if profile data loaded
    if (pstore && jd.count > 0) {
        //manipulate items to get assoc array of hashcodes
        //for the most part json str are goning to be the same
        //unless an update was triggered after getting composite data
        //but before getting the profile
        var items = pstore.items;
        for (var i in items) {
            var jsonstring = items[i];
            var parse = JSON.parse(jsonstring);
            //skip nontrading cards
            if (!(parse.trading_card)) {
                continue;
            }
            var idhash = 'hc' + parse.itemname.hashCode();
            if (cards[idhash]) {
                cards[idhash]['quanity']++;
            } else {
                cards[idhash] = {
                    'itemname': parse.itemname,
                    'quanity': 1
                };
            }
        }

        var badges = pstore.badges;
        for (var j in badges) {
            var badge = badges[j];
            var pos = badge.indexOf(' (Lvl:');
            var badgename = badge.substring(0, pos);
            var sets = badge.substring(pos + 6, pos + 7)
            var idhash = 'g' + badgename.hashCode();
            badgeObj[idhash] = sets;
        }
        if (badgeObj[id]) {
            str = "<td>player has " + badgeObj[id] + " complete set(s)" + " :) ".repeat(badgeObj[id]) + '</td>';
            if (badgeObj[id] == 5) {
                str = "<td>player has completed all 5 sets! :D</td>"
            }
        } else {
            str = "<td>player has no complete sets :(</td>";
        }
        $('#cardlist').prepend("<td>Cards</td>");

        var fid = 'g' + (gamename + ' (Foil)').hashCode();
        if (badgeObj[fid]) {
            str = "<td>player has a complete FOIL set!! XD</td>";
        } else {
            str = "<td>player does not have a complete FOIL set :/</td>";
        }
        $('#inventory').prepend('<td>Player Owns</td>');
        $('#updated').prepend("<td>Updated</td>");
        $('#price').prepend('<td><a target="_blank" href="http://steamcommunity.com/market/search?q=' + gamename + ' trading card">Market Price</a></td>');
    }

    for (var k in jd.cards) {
        var jsonstring = jd.cards[k];
        if (typeof (jsonstring) === "object") {
            parse = jsonstring;
        } else {
            var parse = JSON.parse(jsonstring);
        }
        //skip non trading cards and foils
        if (parse.trading_card == true && parse.itemtype.indexOf('Foil') == -1) {
            var hash = 'hc' + parse.itemname.hashCode();
            $('#cardlist').append('<td>' + parse.itemname + '</td>');
            $('#price').append('<td>' + parse.price + '</td>');
            $('#updated').append('<td>' + parse.updated + '</td>');
            if (cards[hash]) {
                str = parse.itemname + ' (' + cards[hash]['quanity'] + ')';
            } else {
                str = "&nbsp;";
            }
            $('#inventory').append('<td>' + str + '</td>');
        }
    }

    for (var k in jd.cards) {
        var jsonstring = jd.cards[k];
        if (typeof (jsonstring) === "object") {
            parse = jsonstring;
        } else {
            var parse = JSON.parse(jsonstring);
        }
        //skip nontrading cards
        if (parse.trading_card == true && parse.itemtype.indexOf('Foil') != -1) {
            var hash = 'hc' + parse.itemname.hashCode();
            $('#cardlist').append('<td>' + parse.itemname + '</td>');
            $('#price').append('<td>' + parse.price + '</td>');
            $('#updated').append('<td>' + parse.updated + '</td>');
            if (cards[hash]) {
                str = parse.itemname + ' (' + cards[hash]['quanity'] + ')';
            } else {
                str = "&nbsp;";
            }
            $('#inventory').append('<td>' + str + '</td>');
        }
    }
}

function updatePrice(btn, callback) {
    var jqBtn = $(btn);
    var jqRow = jqBtn.parents('tr:first');

    //button specific info
    var game = jqBtn.attr('value');
    var id = jqBtn.attr('id');

    //row specific info
    var rowclasses = jqRow.attr('class');
    var hashid = jqRow.attr('id');
    var cardcount = jqRow.children('td.cardsowned').html();
    var fcardcount = jqRow.children('td.fcardsowned').html();
    var occs = jqRow.children('td.ccs').html();
    var occfs = jqRow.children('td.ccfs').html();

    console.log("hashcode " + id + " value " + game);

    //set color flag
    jqRow.attr('class', 'info');

    $.getJSON("https://api.chpwner.org/update/price/", {
        'game': game
    }, function (data) {
        //compiled stats
        var count = 0;
        var fcount = 0;
        var sum = 0;
        var fsum = 0;
        var avg = 0;
        var favg = 0;
        var time;

        for (var i in data) {
            var card = data[i];
            time = card.updated;
            if (card.itemtype.indexOf('Foil') == -1) {
                //card is not foil
                sum = sum + card.price;
                count++;
            } else {
                //card is foil
                fsum = fsum + card.price;
                fcount++;
            }
        }
        avg = (sum / count).toFixed(2);
        favg = (fsum / fcount).toFixed(2);

        var ccs = ((count - cardcount) * avg).toFixed(2);
        var ccfs = ((fcount - fcardcount) * favg).toFixed(2);

        jqRow.children('td.jdtime').text(time);
        if (occfs != "Maxed!") {
            jqRow.children('td.ccfs').text(ccfs);
        }
        if (occs != "Maxed!") {
            jqRow.children('td.ccs').text(ccs);
        }
        jqRow.children('td.jdfavg').text(favg);
        jqRow.children('td.jdavg').text(avg);
        jqRow.children('td.jdcount').text(count + '/' + fcount);

        //store them
        store[hashid] = {
            'appid': null,
            'avg': avg,
            'favg': favg,
            'cards': data,
            'ccs': ccs,
            'ccfs': ccfs,
            'count': count,
            'fcount': fcount,
            'sum': sum,
            'fsum': fsum,
            'idhash': hashid,
            'name': game,
            'time': time
        }
        jqRow.attr('class', rowclasses);
        //reset error flag
        console.log(count);
        if (count == fcount){
            jqRow.removeClass('error');
        }
        else{
            jqRow.addClass('error');
        }
    })
        .fail(function (jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.log("Request Failed: " + err);
            var d = new Date();
            var time = d.getTime();
            jqRow.children('td.jdtime').text(time);
            jqRow.attr('class', rowclasses);
        })
        .always(function () {
            callback(btn);
        });
}

var error;

function updateProfile(form) {
    error = null;
    var steamid = form.steamid.value;
    form.steamid.value = "Loading...";
    form.sub.disabled = true;
    form.searchBtn.disabled = true;

    if (pstore.steamid) {
        steamid = pstore.steamid;
    }

    if (!(validateID(steamid))) {
        form.steamid.value = "17 digit steamid required";
        form.sub.disabled = false;
        form.searchBtn.disabled = false;
        return (false);
    }
    
    //unhide the bar
    $('#infobar').attr('style', '');
    var bar = $("#progressbar");
    bar.attr('style','width:0%;');

    console.log(steamid);
    pstore.steamid = steamid;

    //get the profile loading
    $.ajax({
        url: "https://api.chpwner.org/update/profile/",
        data: {
            'steamid': steamid
        },
        type: 'GET'
    }).done(function (data) {
        form.steamid.value = steamid;
        bar.attr('style','width:100%');
        getUser(form);
    })
        .fail(function () {
            alert("error loading profile");
            error = "error";
            form.steamid.value = "Error!";
            form.sub.disabled = false;
            form.searchBtn.disabled = false;
        })
        .always(function () {
            //form.sub.disabled = false;
            //form.searchBtn.disabled = false;
        });

    if (error) {
        return (false);
    }

    //start loading bar
    var data = 0;
    var count = 0;

    ploader(data, count);

    return (true);
}

function ploader(data, count) {
    if (error == "error") {
        return ("error");
    }
    var str = data.toFixed(0) + "% Loaded... ";
    str = str + (count*5) + " seconds passed... ";
    var est = (((count*5) / data) * (100 - data)).toFixed(0);
    str = str + "estimated " + est + " seconds remain";

    $('#stats').text(str);

    if (data < 100) {
        t = setTimeout(function () {
            ajaxCall(count)
        }, 5000);
    }
}

function ajaxCall(count) {
    var data = 0;
    count++;

    $.ajax({
        url: "https://api.chpwner.org/steam/logger/" + pstore.steamid,
        cache: false
    })
        .done(function (data) {            
            $("#progressbar").attr('style',('width:'+data+'%;'));
            data = Number(data);
            ploader(data, count);
        })
        .fail(function () {
            ploader(data, count);
        });
}

function modal(){
    $('#invModal').modal()
}
