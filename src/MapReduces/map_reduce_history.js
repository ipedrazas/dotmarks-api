// MapReduce to extract counts by day

var mapHistoryByDayPerUser = function() {
    if(this.user == "ivan"){
        if (this.time.day) {
            emit(this.time.day, 1); // store a 1 for each word
        }
    }
};


var reduceHistoryByDayPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryByDayPerUser, reduceHistoryByDayPerUser, {out: "ivan_per_day"});


// MapReduce to extract counts by day

var mapHistoryByHoursPerUser = function() {
    if(this.user == "ivan"){
            emit(this.time.hours, 1); // store a 1 for each word
    }
};


var reduceHistoryByHoursPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryByHoursPerUser, reduceHistoryByHoursPerUser, {out: "ivan_per_hours"});


// MapReduce to extract counts per weekday

var mapHistoryPerWeekdayPerUser = function() {
    if(this.user == "ivan"){
            emit(this.time.weekday, 1); // store a 1 for each word
    }
};


var reduceHistoryPerWeekdayPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryPerWeekdayPerUser, reduceHistoryPerWeekdayPerUser, {out: "ivan_per_weekday"});




// MapReduce to extract counts per domain

db.system.js.save(
   {
     _id : "cleanUp" ,
     value : function(url) {
                if(url.search(/^https?\:\/\//) != -1)
                    url = url.match(/^https?\:\/\/([^\/?#]+)(?:[\/?#]|$)/i, "");
                else
                    url = url.match(/^([^\/?#]+)(?:[\/?#]|$)/i, "");
                url[1] = url[1].replace(/^www\./i, "");
                return url[1];
            }
   }
);

var mapHistoryPerDomainPerUser = function() {
    if(this.user == "ivan"){
            emit(cleanUp(this.url), 1); // store a 1 for each word
    }
};


var reduceHistoryPerDomainPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryPerDomainPerUser, reduceHistoryPerDomainPerUser, {out: "ivan_per_domain"});
