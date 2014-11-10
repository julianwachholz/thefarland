/*
 * thefar.land script
 */
(function (w, d) {
    'use strict';

    function urlize(obj) {
        var key, str = '';
        for (key in obj) {
            if (str !== '') {
                str += "&";
            }
            str += key + '=' + encodeURI(obj[key]);
        }
        return str;
    };

    function ajax(method, url, data, callback) {
        var req = new XMLHttpRequest();
        req.open(method, url, true);
        if (method === 'POST') {
            req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        }
        req.addEventListener('load', function () {
            if (this.status >= 200 && this.status < 400) {
                callback(JSON.parse(this.response));
            }
        });
        if (data) {
            req.send(urlize(data));
        } else {
            req.send()
        }
    };

    function verificationCode(url, csrf_token) {
        ajax('POST', url, {csrfmiddlewaretoken: csrf_token}, function (response) {
            if (response.status === 'OK') {
                d.getElementById('verification-step-1').className = 'hidden';
                d.getElementById('verification-step-2').className = '';
            }
        })
    };

    d.addEventListener('DOMContentLoaded', function () {
        d.getElementById('send-verification').addEventListener('click', function (event) {
            event.preventDefault();
            verificationCode(this.getAttribute('data-url'), this.getAttribute('data-csrf'));
        });
    });

} (window, document));
