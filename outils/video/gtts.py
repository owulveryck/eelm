# -*- coding: utf-8 -*-
"""Synthèse vocale Google Cloud, sans bibliothèque : ADC + API REST.
Le jeton d'accès reste en mémoire, il n'est jamais affiché ni écrit."""
import json, os, time, urllib.parse, urllib.request, base64

ADC = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
_tok = {"v": None, "exp": 0}

def _token():
    if _tok["v"] and time.time() < _tok["exp"] - 60:
        return _tok["v"]
    c = json.load(open(ADC))
    data = urllib.parse.urlencode({
        "client_id": c["client_id"], "client_secret": c["client_secret"],
        "refresh_token": c["refresh_token"], "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    r = json.load(urllib.request.urlopen(req, timeout=60))
    _tok["v"], _tok["exp"] = r["access_token"], time.time() + r.get("expires_in", 3600)
    return _tok["v"]

def _project():
    return json.load(open(ADC)).get("quota_project_id", "")

def _call(url, payload=None, method="GET"):
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": "Bearer " + _token(),
        "Content-Type": "application/json; charset=utf-8",
        "x-goog-user-project": _project()})
    try:
        return json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e:
        raise SystemExit("HTTP %s : %s" % (e.code, e.read().decode()[:500]))

def voices(lang="fr-FR"):
    r = _call("https://texttospeech.googleapis.com/v1/voices?languageCode=" + lang)
    return sorted(v["name"] for v in r.get("voices", []))

def synth(texte, path, voix="fr-FR-Neural2-D", rate=1.0, pitch=0.0):
    payload = {"input": {"text": texte},
               "voice": {"languageCode": voix[:5], "name": voix},
               "audioConfig": {"audioEncoding": "MP3", "speakingRate": rate,
                               "sampleRateHertz": 24000}}
    if not voix.startswith(("fr-FR-Chirp", "fr-FR-Studio")):
        payload["audioConfig"]["pitch"] = pitch
    r = _call("https://texttospeech.googleapis.com/v1/text:synthesize", payload, "POST")
    open(path, "wb").write(base64.b64decode(r["audioContent"]))
    return path
