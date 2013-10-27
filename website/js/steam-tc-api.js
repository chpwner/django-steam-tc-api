//some awesome prototypes
//super awesome numerical hash, no really a lifesaver!
String.prototype.hashCode = function () {
    var hash = 0,
        ig, charg;
    if (this.length == 0) return hash;
    for (ig = 0, l = this.length; ig < l; ig++) {
        charg = this.charCodeAt(ig);
        hash = ((hash << 5) - hash) + charg;
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

function loader() {
    //check for loaded currency table
    if (!fx.rates[currency]){
        alert(currency + " not found in rate table");
        return 'error';
    }
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
//globals?
var tr;
var p = "not a null";
var pstore = {};
//globalstore
var store = {};
var raw = [];
var currency = 'USD';
var curpre = '$';
var cursuf = '';

function webstuff(spinner, callback) {
    $.getJSON('https://api.steamcardsheet.com/data/Games/', function (games) {
        raw = games;
    drawTbl(games);
    //hide button
    //var p; is global now
    $("#toggle").click(function () {
        if (p) {
            console.log("unclicked");
            //no need to append, redrawn
            //p.appendTo("#stage");
            p = null;
            redoTbl('hard');
            //$("#datatable").trigger("update");
            $("#toggle").text('Hide Noncard Games');
        } else {
            console.log("clicked");
            p = $("tr.noncardrow").detach();
            redoTbl('hard');
            //$("#datatable").trigger("update");
            $("#toggle").text('Show Noncard Games');
        }
    });
    }).fail(function (jqxhr, textStatus, error) {
        var err = textStatus + ', ' + error;
        $('#error').append('Request Failed ' + err);
    }).always(function(){
        spinner.stop();
    })
}

function drawTbl(games){
   console.log("new table");
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
                    parse.price = fx.convert(parse.price, {from: "USD", to: currency});
                    //override cards with price to get array of prices of cards
                    //jd.cards[j] = parse.price;
                    jd.time = parse.updated;
                    jd.sum = jd.sum + parse.price;
                    jd.count++;
                } else if (parse.trading_card == true && parse.itemtype.indexOf("Foil") != -1) {
                    parse.price = fx.convert(parse.price, {from: "USD", to: currency});
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
                $('#stage').append('<tr id="' + jd.idhash + '" class="cardrow' + flag + '"><td class="jdname">' + jd.name + '</td><td class="jdcount">' + jd.count + '/' + jd.fcount + '</td><td class="cardsowned">0</td><td class="fcardsowned">0</td><td class="percentage">0%</td><td class="lvl">0</td><td class="flvl">0</td><td class="jdavg">' + curpre + jd.avg + cursuf + '</td><td class="jdfavg">' + curpre +  jd.favg + cursuf + '</td><td class="ccs">' + curpre + jd.ccs + cursuf + '</td><td class="ccfs">' + curpre + jd.ccfs + cursuf + '</td><td class="jdtime">' + jd.time + '</td><td><button type="button" class="btn btn-small upbtn" name="update" value="' + jd.name + '" id="' + jd.appid + '" data-loading-text="Loading...">update</button></td><\/tr>');
                c++;
                ctotal = ctotal + jd.count + jd.fcount;
            } else {
              if (p == null){
                $('#stage').append('<tr id="' + jd.idhash + '" class="noncardrow"><td class="jdname">' + jd.name + '</td><td class="jdcount">0</td><td class="cardsowned">0</td><td class="fcardsowned">0</td><td class="percentage">0%</td><td class="lvl">0</td><td class="flvl">0</td><td class="jdavg">0</td><td class="jdfavg">0</td><td class="ccs">0</td><td class="ccfs">0</td><td class="jdtime">0</td><td><button type="button" class="btn btn-small upbtn" name="update" value="' + jd.name + '" id="' + jd.appid + '" data-loading-text="Loading...">update</button></td><\/tr>');
              }
           }
        }
        //some jquery setup
        $('#searchBtn').attr('disabled', false);
        $('#gamecount').text('Game Count: ' + length);
        $('#itemcount').text('Card Count: ' + ctotal);
        $('#badgecount').text('Badge Count: ' + c * 2);
        //load buttons and tablesorter
        //price update button
        $('.upbtn')
        .click(function () {
            var btn = $(this);
            btn.button('loading');
            updatePrice(btn, function (btn) {
                btn.button('reset');
            });
        })
        tableSort();
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

function getUser(form) {
    //redraw table
    redoTbl();

    //disable some buttons
    $('#sub').attr('disabled', true);
    //hide progress bar
    $('#infobar').attr('style', 'display:none');

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
    $.getJSON('https://api.steamcardsheet.com/data/Players/', data, function (profile) {
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
        tableSort();

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
            var idhash = 'hc' + (parse.itemname + parse.itemtype).hashCode();
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
            var hash = 'hc' + (parse.itemname + parse.itemtype).hashCode();
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
        $('#' + id).children('td.ccs').html(curpre + ccs + cursuf);

        var ccfs = ((jd.fcount - fowned) * jd.favg).toFixed(2);
        $('#' + id).children('td.ccfs').html(curpre + ccfs + cursuf);

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


//disable enter key so user has to click buttons
$(document).keypress(
    function (event) {
        if (event.which == '13') {
            event.preventDefault();
        }
    });

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

    console.log("hashcode " + hashid + " value " + game);

    //set color flag
    jqRow.attr('class', 'info');

    $.getJSON("https://api.steamcardsheet.com/update/price/", {
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
            card.price = fx.convert(card.price, {from: "USD", to: currency});
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
            jqRow.children('td.ccfs').html(curpre + ccfs + cursuf);
        }
        if (occs != "Maxed!") {
            jqRow.children('td.ccs').html(curpre + ccs + cursuf);
        }
        jqRow.children('td.jdfavg').html(curpre + favg + cursuf);
        jqRow.children('td.jdavg').html(curpre + avg + cursuf);
        jqRow.children('td.jdcount').text(count + '/' + fcount);

        //store them
        store[hashid] = {
            'appid': id,
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
    }).fail(function (jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.log("Request Failed: " + err);
            var d = new Date();
            var time = d.getTime();
            jqRow.children('td.jdtime').text(time);
            jqRow.attr('class', rowclasses);
    }).always(function () {
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
        url: "https://api.steamcardsheet.com/update/profile/",
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
        url: "https://api.steamcardsheet.com/steam/logger/" + pstore.steamid,
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

function redoTbl(flag){
var tableHTML = '\
        <table class="table table-bordered table-hover tablesorter" id="datatable">\
        <thead>\
        <tr>\
          <th>Name</th>\
          <th>Cards Per Set</th>\
          <th>Cards Owned</th>\
          <th>Foil Cards Owned</th>\
          <th>Percent Complete</th>\
          <th>Complete Sets</th>\
          <th>Complete Foil Sets</th>\
          <th>Avg Card Cost</th>\
          <th>Avg Foil Card Cost</th>\
          <th>Cost to Complete Set</th>\
          <th>Cost to Complete Foil Set</th>\
          <th>Prices Last Updated</th>\
          <th></th>\
        </tr>\
        </thead>\
        <tbody id="stage">\
        </tbody>\
        </table>\
';

//check to see if page is loaded
var checker = $('#stage').html().trim();

if (checker == ""){
console.log("page is not loaded");
return 'page is not loaded';
}

//built in function to revert table
$('#datatable').dataTable().fnDestroy()

if (flag == 'hard'){
    console.log("hard reset");
    $('#tablediv').html(tableHTML);
    drawTbl(raw);
   }else{
    console.log("soft reset");
   }
}

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
    if ($.isEmptyObject(pstore) == false && jd.count > 0) {
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
            var idhash = 'hc' + (parse.itemname + parse.itemtype).hashCode();
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

        var fid = 'g' + (gamename + ' (Foil)').hashCode();
        if (badgeObj[fid]) {
            str = "<td>player has a complete FOIL set!! XD</td>";
        } else {
            str = "<td>player does not have a complete FOIL set :/</td>";
        }
        $('#cardlist').prepend("<td>Cards</td>");
        $('#inventory').prepend('<td><a href="http://steamcommunity.com/profiles/'+pstore.steamid+'/gamecards/'+jd.appid+'">Player</a> <a href="http://steamcommunity.com/profiles/'+pstore.steamid+'/gamecards/'+jd.appid+'/?border=1">Owns</a></td>');
        $('#updated').prepend("<td>Updated</td>");
        $('#price').prepend('<td><a target="_blank" href="http://steamcommunity.com/market/search?q=' + gamename + ' trading card">Market Price</a></td>');
    }else{
        $('#cardlist').prepend("<td>Cards</td>");
        $('#inventory').prepend('<td>Player Owns</td>');
        $('#updated').prepend("<td>Updated</td>");
        $('#price').prepend('<td><a target="_blank" href="http://steamcommunity.com/market/search?q=' + gamename + ' trading card">Market Price</a></td>');
    }

    for (var k in jd.cards) {
        var jsonstring = jd.cards[k];
        if (typeof (jsonstring) === "object") {
            var parse = jsonstring;
            parse.price = (parse.price * 1.0).toFixed(2);
        } else {
            var parse = JSON.parse(jsonstring);
            parse.price = fx.convert(parse.price, {from: "USD", to: currency}).toFixed(2);
        }
        //skip non trading cards and foils
        if (parse.trading_card == true && parse.itemtype.indexOf('Foil') == -1) {
            var hash = 'hc' + (parse.itemname + parse.itemtype).hashCode();
            $('#cardlist').append('<td><a target="_blank" href="http://steamcommunity.com/market/listings/753/' + jd.appid + '-' + parse.itemname + '">' + parse.itemname + '</a></td>');
            $('#price').append('<td>' + curpre + parse.price + cursuf + '</td>');
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
            var parse = jsonstring;
            parse.price = (parse.price * 1.0).toFixed(2);
        } else {
            var parse = JSON.parse(jsonstring);
            parse.price = fx.convert(parse.price, {from: "USD", to: currency}).toFixed(2);
        }
        //skip nontrading cards
        if (parse.trading_card == true && parse.itemtype.indexOf('Foil') != -1) {
            var hash = 'hc' + (parse.itemname + parse.itemtype).hashCode();
            $('#cardlist').append('<td><a target="_blank" href="http://steamcommunity.com/market/listings/753/' + jd.appid + '-' + parse.itemname + '">' + parse.itemname + '</a></td>');
            $('#price').append('<td>' + curpre + parse.price + cursuf + '</td>');
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

function tableSort(){
    console.log("sortify");
    //table sorter

    var attachme = $('#datatable tbody tr');
    //remove old events before attaching new ones
    attachme.off();
    attachme.on('click', function () {
        var nTr = this;
        gameLookup(nTr);
        if ( oTable.fnIsOpen(nTr) )
        {
            /* This row is already open - close it */
            oTable.fnClose( nTr );
            console.log("close");
        }
        else
        {
            /* Open this row */
            oTable.fnOpen( nTr, $('#gameinfo').clone(), "details" );
            $(this).next().find('*').attr('style','background-color:white');
            console.log("open");
        }
    });    

    //$("#datatable").dataTable({"bPaginate": false});
    //$("#datatable").dataTable({"aLengthMenu": [[10, 50, 100, -1], [10, 50, 100, "All"]]});
    var oTable = $('#datatable').dataTable( {
        "aoColumnDefs": [
            { "bSortable": false, "aTargets": [-1] }
        ],
        "aLengthMenu":[[10,50,100,-1],[10,50,100,"All"]]
    });
}

// Load exchange rates data via AJAX:
$.getJSON(
    // NB: using Open Exchange Rates here, but you can use any source!
    'https://api.steamcardsheet.com/steam/js/exchange.json',
    function(data) {
        // Check money.js has finished loading:
        if ( typeof fx !== "undefined" && fx.rates ) {
            fx.rates = data.rates;
            fx.base = data.base;
        } else {
            // If not, apply to fxSetup global:
            var fxSetup = {
                rates : data.rates,
                base : data.base
            }
        }
        
        var cookie = getCookie('chpwner');
        if (cookie == 1){
            loader();
            setCookie('chpwner',0,1);
        }
    }
)

function curr()
{
var select=document.getElementById("moneyList");
currency=select.options[select.selectedIndex].text;

//check for loaded currency table
if (!fx.rates[currency]){
    alert(currency + " not found in rate table");
    return 'error';
}

curpre = '';
cursuf = '';

switch(currency)
{
case 'USD':
  curpre = '&#36;';
  break;
case 'EUR':
  curpre = '&#128;';
  break;
case 'BRL':
  curpre = 'R$';
  break;
case 'GBP':
  curpre = '&#163;';
  break;
case 'RUB':
  cursuf=" &#1088;&#1091&#1073;";
  break;
case 'CAD':
  curpre = 'C$';
  break;
case 'JPY':
  curpre = '&#165;';
  break;
case 'INR':
  curpre = '&#8377;';
  break;
default:
  curpre = '';
}

//have to reset table to USD values
redoTbl('hard');
}
