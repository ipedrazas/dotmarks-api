// MapReduce to extract counts by day

var mapHistoryByDayPerUser = function() {
    key = {
        day: this.time.day,
        user: this.user
    };
    emit(key, 1);
};


var reduceHistoryByDayPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryByDayPerUser, reduceHistoryByDayPerUser, {out: "per_day"});


// MapReduce to extract counts by day

var mapHistoryByHoursPerUser = function() {
    key = {
        hours: this.time.hours,
        user: this.user
    };
    emit(key, 1);
};


var reduceHistoryByHoursPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryByHoursPerUser, reduceHistoryByHoursPerUser, {out: "per_hours"});


// MapReduce to extract counts per weekday

var mapHistoryPerWeekdayPerUser = function() {
    key = {
        weekday: this.time.weekday,
        user: this.user
    };
    emit(key, 1); // store a 1 for each word
};


var reduceHistoryPerWeekdayPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryPerWeekdayPerUser, reduceHistoryPerWeekdayPerUser, {out: "per_weekday"});




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
    key = {
        url: cleanUp(this.url),
        user: this.user
    };
    emit(cleanUp(key, 1); // store a 1 for each word

};


var reduceHistoryPerDomainPerUser = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.history.mapReduce(mapHistoryPerDomainPerUser, reduceHistoryPerDomainPerUser, {out: "per_domain"});

