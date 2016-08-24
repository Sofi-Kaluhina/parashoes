/**
 * Created by sofi on 02.06.16.
 */

// 1
for (var i = 0; 1 < 5; i++) {
    (function (j) {
        setTimeout(function () {
            console.log(j);
        }, 200);
    })(i);
}


for (var i = 0; 1 < 5; i++) { // заменить var на let, который создает переменную локально внутри for (который вообще-то не имеет своего скоупа)
    setTimeout(function () {
        console.log(i);
    }, 200);
}

//2

//console.log(h); // хороший пример по скоупу для собеседований
//
//var h = 5;
//
//function setNew() {
//    console.log(h);
//    var h = 5;
//}
//
//var d = setNew();
//console.log(h);

//3 - обращение к данным

var num = 1;
var symb = 'a';
var obj = {
    d: 4
};

function change(val) {
    val = 'new';
}
function changeObj(o) {
    o.c = 5;
}
change(num); // 1, потому что val поменялся, а на num это не повлияло, т к val локальный
change(symb); // 'new'
change(obj); // d: 4, потому что 'new' записалось в другую область памяти, а obj не поменялся (объекты работают по ссылке на область памяти)
changeObj(obj); // d: 4, c: 5, т к мы обращаемся по точке к нашему объекту и дополняем его, а не записываем новый

arr = [1,2, 'a', 'b', [5, 6]];
obj = {a: 1, b: 4, c: {n: 8}};

arr[1] //2
arr[4][0] //5 - идем по массиву в массиве

// способы вывести 1 из объекта:
var key = 'a'; // передаем переменной значение 'a', а потом обращаемся к key

obj.a //1
obj['a'] // 1
obj[key] //1


[1, 5, 10, 4].sort(); // 1, 10, 4, 5 - сортирует как строки (в алфавитном порядке)

// 4 - рекурсия (факториал)

function fact(n) { // передаем в n значение 3
    if ( n<= 0 ) {return 0;}
    var sum = n; // 3 (каждый раз sum = n - 1)
    sum +=fact(--n); // каждый раз вызываем ф-цию со значением n меньше на 1 и складываем с суммой
    return sum;
}

fact(3); //6


// 5 - прототипы

// 1)
var g = 5;

Number.prototype.inc = function() { // ф-ция инкремент в прототипе числа, которая создает его новый метод - инкремент
    return this + 1;
};
console.log(g.inc()); //6

// 2)
var func = function() {
    this.a = 1;
    this.b = 2;
};

func.prototype.c = {n: 3, m: 4};

var o = new func();

for (var key in o) {
    if(o.hasOwnProperty(key)) {
        console.log(key);     // 1, 2
    }
}

// 6 - then в js без ангуляра

function req () {
    var successFunct;
    req.onreadystatechange = function(aEvt) {
        if(req.status === 200) {
            successFunct();
        }
    };
    return {
        then: function(functSuccess) {
            successFunct = functSuccess;
            return this;
        }
    }
}
req('/api/users').then(function() {
    console.log('1');
});
