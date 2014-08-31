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