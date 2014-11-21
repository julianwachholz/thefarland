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
    }

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
            req.send();
        }
    }

    function verificationCode(url, csrf_token) {
        ajax('POST', url, {csrfmiddlewaretoken: csrf_token}, function (response) {
            if (response.status === 'OK') {
                d.getElementById('verification-step-1').className = 'hidden';
                d.getElementById('verification-step-2').className = '';
            }
        });
    }

    function toggleSpectator(url, csrf_token) {
        var status = d.getElementById('gm-spectator-stats');
        status.innerHTML = 'Loading...';

        ajax('POST', url, {csrfmiddlewaretoken: csrf_token}, function (response) {
            if (response.status === 'OK') {
                if (response.gamemode === 3) {
                    status.innerHTML = '<p>Your coordinates:</p><table>' +
                        '<tr><th>X</th><td>' + response.x + '</td></tr>' +
                        '<tr><th>Y</th><td>' + response.y + '</td></tr>' +
                        '<tr><th>Z</th><td>' + response.z + '</td></tr>' +
                    '</table>';
                } else {
                    status.innerHTML = '<p>Switched back to Survival.</p>';
                }
            } else {
                status.className = 'alert-box alert';
                status.innerHTML = response.error;
            }
        });
    }

    function actionButton(id, callback) {
        var button = d.getElementById(id);
        if (button) {
            button.addEventListener('click', function (event) {
                event.preventDefault();
                callback(this.getAttribute('data-url'), this.getAttribute('data-csrf'));
            });
        }
    }

    d.addEventListener('DOMContentLoaded', function () {
        actionButton('send-verification', verificationCode);
        actionButton('gm-spectator', toggleSpectator);
    });

} (window, document));
