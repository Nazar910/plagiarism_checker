import * as assert from 'assert';

async function getJson (args = {}) {
    const { token, url } = args;
    assert.ok(token, 'Token is required');
    assert.ok(url, 'Url is required');
    const r = await fetch(url, {
        headers: {
            Authorization: 'Bearer ' + token
        }
    });
    if (r.status === 401) {
        throw new Error('Unauthorized');
    }
    return await r.json();
}

async function postJson (args = {}) {
    const { body, url, token } = args;
    assert.ok(body, 'Body is required');
    assert.ok(url, 'Url is required');
    const r = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(body)
    });
    if (r.status === 401) {
        throw new Error('Unauthorized');
    }
    return await r.json();
}

export async function getProfile ({ token } = {}) {
    return getJson({
        url: '/api/profile',
        token
    })
}

export async function postLogin ({ email, password }) {
    assert.ok(email, 'Email is required');
    assert.ok(password, 'Password is required');
    const { token } = await postJson({
        url: '/api/auth',
        body: {
            email, password
        }
    });
    return token;
}

export async function checkForPlagiarism ({ token, text }) {
    assert.ok(text, 'Text is required');
    assert.ok(token, 'Token is required');
    return postJson({
        url: '/api/check-for-plagiarism',
        body: {
            text
        },
        token
    });
}
