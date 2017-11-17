"use strict";
/*
Copyright © 2017 Niklas Sombert <niklas@ytvwld.de>
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING file for more details.
*/

function update()
{
  fetch("/data.json").then(function(response)
  {
    response.json().then(function(data)
    {
      document.getElementById("value").innerText = data["value"]? "ja" : "nein";
    });
  });
}

function init()
{
  setInterval(update, 1 * 60 * 10); // every minute
}

window.onload = init;

console.log("You might want to take a look at https://github.com/YtvwlD/freistunde :)");
