#include <QtMath>
#include <QApplication>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QGraphicsEllipseItem>
#include <QThread>
#include <QMutex>

const int WIDTH = 1000;
const int HEIGHT = 1000;
const int PLANET_COUNT = 8;

class PlanetThread : public QThread {
 public:
  PlanetThread(QGraphicsEllipseItem *planet, int angle, int distance)
      : planet_(planet), angle_(angle), distance_(distance) {}

  void run() override {
    while (true) {
      angle_ = (angle_ + 2) % 360;
      int x = distance_ * qCos(angle_);
      int y = distance_ * qSin(angle_);
      planet_->setPos(WIDTH / 2 + x, HEIGHT / 2 + y);
      QThread::msleep(16);
    }
  }

 private:
  QGraphicsEllipseItem *planet_;
  int angle_;
  int distance_;
};

int main(int argc, char *argv[]) {
  QApplication app(argc, argv);

  QGraphicsScene scene;
  scene.setSceneRect(0, 0, WIDTH, HEIGHT);

  QGraphicsView view(&scene);
  view.setRenderHint(QPainter::Antialiasing);
  view.setViewportUpdateMode(QGraphicsView::BoundingRectViewportUpdate);
  view.setBackgroundBrush(Qt::black);
  view.setWindowTitle("Solar System Simulation");
  view.resize(WIDTH, HEIGHT);
  view.show();

  QList<PlanetThread *> threads;
  for (int i = 0; i < PLANET_COUNT; i++) {
    QGraphicsEllipseItem *planet = new QGraphicsEllipseItem();
    planet->setBrush(Qt::white);
    int size = (i + 1) * 10;
    planet->setRect(-size / 2, -size / 2, size, size);
    planet->setPos(WIDTH / 2, HEIGHT / 2);
    scene.addItem(planet);

    int angle = 0;
    int distance = (i + 1) * 100;
    PlanetThread *thread = new PlanetThread(planet, angle, distance);
    threads.append(thread);
    thread->start();
  }

  return app.exec();
}
