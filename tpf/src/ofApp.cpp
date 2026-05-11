#include "ofApp.h"

//--------------------------------------------------------------
void Rectangle::setup(int rndSize = 150, int lifeLength = 200) {
    size.set(ofRandom(10, rndSize), ofRandom(20, rndSize));
    pos.set(ofRandom(ofGetWidth()), ofRandom(ofGetHeight()));
    vel.set(ofRandom(-2, 2), ofRandom(-2, 2));
    life = ofRandom(5, lifeLength);
    
    col = ofColor(ofRandom(150), ofRandom(50), ofRandom(50));
    
    resizeUpdate = false;
}

void Rectangle::update() {
    posM = pos + vel;
    
    bounce_to_bounds();
    
    if(resizeUpdate == true) {
        timer = ofRandom(30, 70);
        if(inc % timer == 0) {
            size.x = ofRandom(200);
            size.y = ofRandom(200);
            inc = 0;
        }
        inc++;
    }
}

void Rectangle::draw() {
    ofPushStyle();
    ofSetColor(col);
    ofDrawRectangle(pos.x, pos.y, size.x, size.y);
    ofPopStyle();
    //ofSetColor(ofRandom(255), ofRandom(255), ofRandom(255));
}

void Rectangle::move(int x, int y) {
    if(vel.x >= 0) {
        pos.x += x;
    }
    else {
        pos.x -= x;
    }
    if(vel.y >= 0) {
        pos.y += y;
    }
    else {
        pos.y -= y;
    }
}

void Rectangle::resize() {
    size.x = ofRandom(200);
    size.y = ofRandom(200);
}

void Rectangle::bounce_to_bounds() {
    if(pos.x <= size.x || pos.x >= ofGetWidth() - size.x) {
        vel.x = vel.x * -1;
        pos.x = ofClamp(pos.x, size.x, ofGetWidth() - size.x);
    }
    if(pos.y <= size.y || pos.y >= ofGetHeight() - size.y) {
        vel.y = vel.y * -1;
        pos.y = ofClamp(pos.y, size.y, ofGetHeight() - size.y);
    }
}
//--------------------------------------------------------------

//--------------------------------------------------------------
void Particule::setup(int radiusMin = 1, int radiusMax = 5) {
    radius = ofRandom(radiusMin, radiusMax);
    pos.set(ofRandom(ofGetWidth()), ofRandom(ofGetHeight()));
    vel.set(ofRandom(-2, 2), ofRandom(-2, 2));
    
    gravity = 0.1;
    friction = 0.99;
    forceMul = 0.6;
}

void Particule::update() {
    //on ajoute du vent
    vel += (wind * (1/radius));
    vel.limit(3);
    
    //force attracteur
    ofVec2f force_att = attractor_pos - pos;
    force_att.limit(0.25);
    
    //force répulseur
    ofVec2f force_rep = repulsor_pos - pos;
    force_rep.limit(0.25);
    
    //on combine les forces
    ofVec2f force = force_att + -force_rep;
    
    //utiliser la force
    vel += force * forceMul;
    
    //update pos
    pos = pos + vel;
    
    //reste donc dans le canevas!!
    wrap_to_bounds();
}

void Particule::draw() {
    ofPushStyle();
    ofSetColor(ofNoise(ofGetElapsedTimef() * 1.0) * 255, col.g, col.b);
    ofDrawCircle(pos.x, pos.y, radius);
    ofPopStyle();
}


void Particule::bounce_to_bounds() {
    if(pos.x <= radius || pos.x >= ofGetWidth() - radius) {
        vel.x = vel.x * -1;
        pos.x = ofClamp(pos.x, radius, ofGetWidth() - radius);
    }
    if(pos.y <= radius || pos.y >= ofGetHeight() - radius) {
        vel.y = vel.y * -1;
        pos.y = ofClamp(pos.y, radius, ofGetHeight() - radius);
    }
}

void Particule::wrap_to_bounds() {
    if(pos.x < 0) {
        pos.x = ofGetWidth();
    }
    if(pos.x > ofGetWidth()) {
        pos.x = 0;
    }
    if(pos.y < 0) {
        pos.y = ofGetHeight();
    }
    if(pos.y > ofGetHeight()) {
        pos.y = 0;
    }
}
//--------------------------------------------------------------

//--------------------------------------------------------------
void Strobe::setup(float iStrobes, float nStrobes = 1, bool isHorizontal = false) {
    if(isHorizontal == true) {
        if(nStrobes == 1) {
            size.set(ofGetWidth() / 2, ofGetHeight() / 2);
            pos.set((ofGetWidth() / 2) - (size.x / 2), (ofGetHeight() / 2) - (size.y / 2));
        }
        else {
            size.set(ofGetWidth(), (ofGetHeight() / nStrobes) - size.y);
            pos.set(0, size.y * iStrobes);
        }
    }
    else {
        if(nStrobes == 1) {
            size.set(ofGetWidth() / 2, ofGetHeight() / 2);
            pos.set((ofGetWidth() / 2) - (size.x / 2), (ofGetHeight() / 2) - (size.y / 2));
        }
        else {
            size.set((ofGetWidth() / nStrobes) - size.x, ofGetHeight());
            pos.set(size.x * iStrobes, 0);
        }
    }
    
    fade = 0;
    pAlpha.x = 0.5;
}

void Strobe::update() {
    pAlpha.y = (pAlpha.x * ofRandom(0.8, 1.2)) - ((fade * ofGetElapsedTimeMillis()) * ofRandom(0.5, 1.5));
}

void Strobe::draw() {
    ofPushStyle();
    ofSetColor(col, pAlpha.y * 150);
    ofDrawRectangle(pos.x, pos.y, size.x, size.y);
    ofPopStyle();
}

void Strobe::fadeOut() {
    fade = 0.00008;
    ofResetElapsedTimeCounter();
}
//--------------------------------------------------------------

//--------------------------------------------------------------
void ofApp::setup(){
    ofSetWindowPosition(0, -1050);
    ofToggleFullscreen();
    ofBackground(0);
    ofSetVerticalSync(true);
    ofSetFrameRate(60);
    
    fbo.allocate(ofGetWidth(), ofGetHeight(), GL_RGBA);
    
    attracteur.setup();
    repulseur.setup();
    
    receiver.setup(9002);
    alpha_trail_fbo = 25.5;
    
    //fbo_brcosa.allocate(ofGetWidth(), ofGetHeight(), GL_RGBA);
    //sh_brcosa.load("brcosa");
    //img.allocate(ofGetWidth(), ofGetHeight(), OF_IMAGE_COLOR);
}

//--------------------------------------------------------------
void ofApp::update(){
    // check for waiting messages
    while(receiver.hasWaitingMessages()) {
        // get the next message
        ofxOscMessage m;
        receiver.getNextMessage(m);
        // check for mouse moved message
        if(m.getAddress() == "/BPM") {
            for(int i=0; i<myRectangle.size(); i++) {
                if(myRectangle[i].life <= 0) {
                    myRectangle[i].life = m.getArgAsInt(2) * ofRandom(0.75, 1.25);
                }
            }
            for(int i=0; i<myParticules.size(); i++) {
                myParticules[i].forceMul = m.getArgAsFloat(0) / 20;
            }
            for(int i=0; i<myStrobe.size(); i++) {
                myStrobe[i].pAlpha.x = m.getArgAsInt(0) / 1024.0;
            }
        }
        if(m.getAddress() == "/start") {
            switchScene();
        }
    }
    
    // Rectangle
    for(int i=0; i<myRectangle.size(); i++) {
        myRectangle[i].update();
        myRectangle[i].life -= 1;
        if(myRectangle[i].life == 0) {
            myRectangle[i].move(myRectangle[i].posM.x, myRectangle[i].posM.y);
            myRectangle[i].life = ofRandom(10, 200);
            inc = 0;
        }
    }
    
    // Particule
    attracteur.update();
    repulseur.update();
    
    for(int i=0; i<myParticules.size(); i++) {
        myParticules[i].wind = vent;
        myParticules[i].attractor_pos = attracteur.pos;
        myParticules[i].repulsor_pos = repulseur.pos;
        //myParticules[i].update();
    }
    
    for(int i=0; i<myParticules.size(); i++) {
        myParticules[i].update();
    }
    
    for(int i=0; i<myStrobe.size(); i++) {
        myStrobe[i].update();
    }
    
    ofSetWindowTitle(ofToString(ofGetFrameRate()));
}

//--------------------------------------------------------------
void ofApp::draw(){
    fbo.begin();
    //dessine un background noir avec alpha pour motion blur
    ofPushStyle();
    ofSetColor(0, alpha_trail_fbo);
    ofDrawRectangle(0, 0, ofGetWidth(), ofGetHeight());
    ofPopStyle();
    
    ofEnableBlendMode(OF_BLENDMODE_DISABLED);
    for(int i=0; i<myRectangle.size(); i++) {
        ofEnableBlendMode(OF_BLENDMODE_MULTIPLY);
        myRectangle[i].draw();
    }
    for(int i=0; i<myStrobe.size(); i++) {
        switch(draw_mode) {
            case 0:
                ofEnableBlendMode(OF_BLENDMODE_ALPHA);
                break;
            case 1:
                ofEnableBlendMode(OF_BLENDMODE_ADD);
                break;
            case 2:
                ofEnableBlendMode(OF_BLENDMODE_SCREEN);
                break;
            case 3:
                ofEnableBlendMode(OF_BLENDMODE_MULTIPLY);
                break;
        }
        myStrobe[i].draw();
    }
    
    for(int i=0; i<myParticules.size(); i++) {
        ofEnableBlendMode(OF_BLENDMODE_SCREEN);
        myParticules[i].draw();
    }
    
    fbo.end();
    /*
    fbo_brcosa.begin();
    ofClear(0, 255);
    
    sh_brcosa.begin();
    sh_brcosa.setUniform1f("brightness", brightness);
    sh_brcosa.setUniform1f("contrast", contrast);
    sh_brcosa.setUniform1f("saturation", saturation);
    sh_brcosa.setUniformTexture("tex0", fbo.getTexture(), 1);
    img.draw(0, 0, 1280, 720);
    sh_brcosa.end();
    fbo_brcosa.end();
    
    fbo_brcosa.draw(0, 0);
    */
    fbo.draw(0, 0);
}

//--------------------------------------------------------------
void ofApp::switchScene(){
    switch(tSwitch) {
        case 0: {
            cout <<tSwitch;
            
            int nStrobes = 2;
            for(int i=0; i<nStrobes; i++) {
                Strobe s;
                s.setup(i, nStrobes);
                myStrobe.push_back(s);
            }
            break;
        }
        case 1: {
            cout <<tSwitch;
            
            int nStrobes = 800;
            for(int i=0; i<nStrobes; i++) {
                Strobe s;
                s.setup(i, nStrobes);
                myStrobe.push_back(s);
            }
            break;
        }
        case 2: {
            cout << tSwitch;
            
            draw_mode = 0;
            for(int i=0; i<2; i++) {
                myStrobe[i].col = ofColor(ofRandom(255), ofRandom(255), ofRandom(255));
            }
            int nStrobes = 12;
            for(int i=0; i<nStrobes; i++) {
                Strobe s;
                s.setup(i, nStrobes, true);
                myStrobe[i].col = ofColor(ofRandom(50), ofRandom(50), ofRandom(255));
                myStrobe.push_back(s);
            }
            break;
        }
        case 3: {
            //ici
            cout <<tSwitch;
            
            draw_mode = 1;
            int nRectangles = 80;
            for(int i=0; i<nRectangles; i++) {
                Rectangle r;
                r.setup(150, 50);
                myRectangle.push_back(r);
            }
            break;
        }
        case 4: {
            cout <<tSwitch;
            
            int nRectangles = 800;
            for(int i=0; i<nRectangles; i++) {
                Rectangle r;
                r.setup(15, 10);
                myRectangle.push_back(r);
            }
            for(int i=0; i<2; i++) {
                myStrobe[i].col = ofColor(ofRandom(255), ofRandom(150), ofRandom(150));
            }
            for(int i=0; i<myRectangle.size(); i++) {
                myRectangle[i].resizeUpdate = true;
            }
            break;
        }
        case 5: {
            cout <<tSwitch;
            
            for(int i=0; i<2; i++) {
                myStrobe[i].col = ofColor(ofRandom(255), ofRandom(50), ofRandom(50));
            }
            draw_mode = 3;
            int nParticles = 1200;
            for(int i=0; i<nParticles; i++) {
                Particule p;
                p.setup();
                myParticules.push_back(p);
            }
            break;
        }
        case 6: {
            //ici
            cout <<tSwitch;
            
            draw_mode = 1;
            int nStrobes = 800;
            for(int i=0; i<nStrobes; i++) {
                Strobe s;
                s.setup(i, nStrobes, true);
                myStrobe[i].col = ofColor(ofRandom(255), ofRandom(50), ofRandom(50));
                myStrobe.push_back(s);
            }
            break;
        }
        case 7: {
            cout <<tSwitch;
            
            draw_mode = 3;
            myRectangle.erase(myRectangle.begin(), myRectangle.begin()+myRectangle.size());
            
            Strobe s;
            s.setup(0, 1);
            myStrobe[myStrobe.size()].col = ofColor(ofRandom(15), ofRandom(15), ofRandom(15));
            myStrobe.push_back(s);
            
            int nRectangles = 600;
            for(int i=0; i<nRectangles; i++) {
                Rectangle r;
                r.setup(30, 20);
                myRectangle.push_back(r);
            }
            break;
        }
        case 8: {
            cout <<tSwitch;
            
            
            myParticules.erase(myParticules.begin(), myParticules.begin()+1200);
            int nParticles = 400;
            for(int i=0; i<nParticles; i++) {
                Particule p;
                p.setup(30, 70);
                myParticules.push_back(p);
            }
            break;
        }
        case 9: {
            cout <<tSwitch;
            
            draw_mode = 1;
            myRectangle.erase(myRectangle.begin(), myRectangle.begin()+myRectangle.size());
            myParticules.erase(myParticules.begin(), myParticules.begin()+myParticules.size());
            for(int i=0; i<myStrobe.size(); i++) {
                myStrobe[i].col = ofColor(ofRandom(25), ofRandom(25), ofRandom(25));
            }
            break;
        }
        case 10: {
            cout <<tSwitch;
            
            for(int i=0; i<myStrobe.size(); i++) {
                myStrobe[i].fadeOut();
            }
            break;
        }
    }
    tSwitch += 1;
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    if(key == 'r') {
        for(int i=0; i<myRectangle.size(); i++) {
            myRectangle[i].resize();
        }
    }
    if(key == 'c') {
        for(int i=0; i<myParticules.size(); i++) {
            myParticules[i].col = ofColor(ofRandom(255), ofRandom(255), ofRandom(255));
        }
    }
    if(key == 'v') {
        draw_mode = ofRandom(4);
        cout << draw_mode;
    }
    if(key == OF_KEY_RIGHT) {
        switchScene();
    }
    /*if(key == 'b') {
        brightness = ofRandom(1.0);
        contrast = ofRandom(1.0);
        saturation = ofRandom(1.0);
    }*/
    if (key == 's') {
        cout << myStrobe.size();
        //cout << myParticules.size();
        //cout << myRectangle.size();
    }
    if(key == 'f') {
        ofToggleFullscreen();
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
