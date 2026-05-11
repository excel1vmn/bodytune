#pragma once

#include "ofMain.h"
#include "ofxOsc.h"

class Rectangle{
public:
    //Construtor
    Rectangle() {}

    //Functions
    void setup(int rndSize, int lifeLength);
    void update();
    void draw();

    void move(int x, int y);
    void resize();
    void bounce_to_bounds();
    
    //Attributes
    ofVec2f size, pos, posM, vel;
    int life;
    int inc, timer;
    ofColor col;
    bool resizeUpdate;
};

class Particule{
public:
    //ze constructeur
    Particule() {}
    
    //ze méthodes
    void setup(int radiusMin, int radiusMax);
    void update();
    void draw();
    void bounce_to_bounds();
    void wrap_to_bounds();
    
    //ze attributs
    ofVec2f vel, pos, wind;
    ofVec2f attractor_pos, repulsor_pos;
    float radius, gravity, friction, forceMul;
    ofColor col;
};

class Strobe{
public:
    //Constructor
    Strobe() {}
    
    //Functions
    void setup(float iStrobes, float nStrobes, bool isHorizontal);
    void update();
    void draw();
    
    void fadeOut();
    
    ofVec2f size, pos, pAlpha;
    float fade;
    ofColor col;
};

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();
    
        void switchScene();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void mouseEntered(int x, int y);
		void mouseExited(int x, int y);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
		
    ofxOscReceiver receiver;
    ofFbo fbo;
    vector <Rectangle> myRectangle;
    vector <Particule> myParticules;
    vector <Strobe> myStrobe;
    
    Particule attracteur, repulseur;
    
    ofVec2f vent;
    int alpha_trail_fbo;
    int inc, draw_mode, tSwitch;
    
    /*
    ofFbo fbo_brcosa;
    ofShader sh_brcosa;
    float brightness, contrast, saturation;
    ofImage img;
     */
};
