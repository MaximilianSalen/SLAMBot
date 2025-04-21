#define GL_GLEXT_PROTOTYPES
#include <pangolin/pangolin.h>

void TestPangolinWindow()
{
    // Create OpenGL window in single line
    pangolin::CreateWindowAndBind("Hello Pangolin", 640, 480);

    // Setup the OpenGL context
    glEnable(GL_DEPTH_TEST);

    // Define a simple camera render object (for 3D, optional here)
    pangolin::OpenGlRenderState s_cam(
        pangolin::ProjectionMatrix(640,480,420,420,320,240,0.2,100),
        pangolin::ModelViewLookAt(0,0,-1, 0,0,0, pangolin::AxisY)
    );

    // Create an interactive viewport
    pangolin::Handler3D handler(s_cam);
    pangolin::View& d_cam = pangolin::CreateDisplay()
        .SetBounds(0.0, 1.0, 0.0, 1.0, -640.0f/480.0f)
        .SetHandler(&handler);

    // Main loop
    while (!pangolin::ShouldQuit())
    {
        // Clear screen and activate view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        d_cam.Activate(s_cam);

        // Draw something basic
        pangolin::glDrawColouredCube();

        // Swap frames and process events
        pangolin::FinishFrame();
    }
}
