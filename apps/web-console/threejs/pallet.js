import * as THREE from 'three';
//导入轨道控制器
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
//导入lil-GUI
import { GUI } from 'three/addons/libs/lil-gui.module.min.js'
// mockData
// import { mockData } from './mockData';
const mockData = {
    singleContainerLoadingSolutions: [
      {
        container: {
          containerId: 'container',
          cube: {
            height: 2698,
            length: 12032,
            volume: 76351414272,
            width: 2352,
          },
          price: 3400.0,
          volume: 76351414272,
          weight: 30400.0,
        },
        placedItems: [
          {
            itemId: 'EBD0100000074785',
            orientation: 'FRONT_DOWN',
            position: { x: 0, y: 0, z: 0 },
            rotatedCube: {
              height: 1140,
              length: 1270,
              volume: 1867662000,
              width: 1290,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 1270, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 2470, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 3670, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 4870, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 0, z: 1140 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089800',
            orientation: 'FRONT_UP',
            position: { x: 6070, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 7270, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 1200, y: 0, z: 1160 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 8470, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 2400, y: 0, z: 1160 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'FRONT_UP',
            position: { x: 9670, y: 0, z: 0 },
            rotatedCube: {
              height: 1160,
              length: 1200,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000089801',
            orientation: 'BOTTOM_UP',
            position: { x: 10870, y: 0, z: 0 },
            rotatedCube: {
              height: 1200,
              length: 1160,
              volume: 1670400000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 1290, z: 0 },
            rotatedCube: {
              height: 500,
              length: 3480,
              volume: 1513800000,
              width: 870,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 1290, z: 500 },
            rotatedCube: {
              height: 500,
              length: 3480,
              volume: 1513800000,
              width: 870,
            },
          },
          {
            itemId: 'EBD010220600022',
            orientation: 'FRONT_UP',
            position: { x: 3480, y: 1200, z: 0 },
            rotatedCube: {
              height: 550,
              length: 1980,
              volume: 1056330000,
              width: 970,
            },
          },
          {
            itemId: 'EBD0100000072512',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 1290, z: 1000 },
            rotatedCube: {
              height: 750,
              length: 1380,
              volume: 1055700000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD0100000072513',
            orientation: 'FRONT_UP',
            position: { x: 5460, y: 1200, z: 0 },
            rotatedCube: {
              height: 750,
              length: 1380,
              volume: 1055700000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD010220600023',
            orientation: 'FRONT_UP',
            position: { x: 3480, y: 1200, z: 550 },
            rotatedCube: {
              height: 750,
              length: 1380,
              volume: 1055700000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD0100000083503',
            orientation: 'SIDE_UP',
            position: { x: 1380, y: 1200, z: 1000 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1009800000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000083503',
            orientation: 'SIDE_UP',
            position: { x: 6840, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1009800000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000072510',
            orientation: 'SIDE_UP',
            position: { x: 2400, y: 1200, z: 1000 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 7860, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 8880, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 4860, y: 1200, z: 750 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 0, y: 1200, z: 1750 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'SIDE_UP',
            position: { x: 9900, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'FRONT_UP',
            position: { x: 10920, y: 1200, z: 0 },
            rotatedCube: {
              height: 900,
              length: 1090,
              volume: 1000620000,
              width: 1020,
            },
          },
          {
            itemId: 'EBD010220600025',
            orientation: 'SIDE_UP',
            position: { x: 3600, y: 0, z: 1160 },
            rotatedCube: {
              height: 900,
              length: 1020,
              volume: 1000620000,
              width: 1090,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 3420, y: 1200, z: 1300 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'BOTTOM_UP',
            position: { x: 5880, y: 1200, z: 750 },
            rotatedCube: {
              height: 1010,
              length: 900,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 4620, y: 0, z: 1160 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 6780, y: 1200, z: 900 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 5630, y: 0, z: 1160 },
            rotatedCube: {
              height: 900,
              length: 1010,
              volume: 999900000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_UP',
            position: { x: 7790, y: 1200, z: 900 },
            rotatedCube: {
              height: 850,
              length: 1080,
              volume: 991440000,
              width: 1080,
            },
          },
          {
            itemId: 'EBD010220600021',
            orientation: 'FRONT_UP',
            position: { x: 1020, y: 1200, z: 1900 },
            rotatedCube: {
              height: 550,
              length: 1980,
              volume: 838530000,
              width: 770,
            },
          },
          {
            itemId: 'EBD010220600024',
            orientation: 'FRONT_UP',
            position: { x: 6640, y: 0, z: 1160 },
            rotatedCube: {
              height: 550,
              length: 1980,
              volume: 838530000,
              width: 770,
            },
          },
          {
            itemId: 'EBD0100000084194',
            orientation: 'FRONT_UP',
            position: { x: 6640, y: 770, z: 1160 },
            rotatedCube: {
              height: 550,
              length: 3430,
              volume: 792330000,
              width: 420,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'SIDE_UP',
            position: { x: 4430, y: 1100, z: 1650 },
            rotatedCube: {
              height: 660,
              length: 800,
              volume: 580800000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_UP',
            position: { x: 8870, y: 1200, z: 900 },
            rotatedCube: {
              height: 600,
              length: 1200,
              volume: 576000000,
              width: 800,
            },
          },
          {
            itemId: 'EBD0100000072510',
            orientation: 'BOTTOM_UP',
            position: { x: 5230, y: 1100, z: 1760 },
            rotatedCube: {
              height: 770,
              length: 850,
              volume: 575960000,
              width: 880,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'BOTTOM_UP',
            position: { x: 10070, y: 1200, z: 900 },
            rotatedCube: {
              height: 770,
              length: 850,
              volume: 575960000,
              width: 880,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'FRONT_UP',
            position: { x: 8620, y: 0, z: 1160 },
            rotatedCube: {
              height: 850,
              length: 880,
              volume: 575960000,
              width: 770,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'BOTTOM_UP',
            position: { x: 3600, y: 0, z: 2060 },
            rotatedCube: {
              height: 600,
              length: 660,
              volume: 475200000,
              width: 1200,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_UP',
            position: { x: 9500, y: 0, z: 1200 },
            rotatedCube: {
              height: 500,
              length: 1480,
              volume: 458800000,
              width: 620,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_UP',
            position: { x: 4260, y: 0, z: 2060 },
            rotatedCube: {
              height: 500,
              length: 1480,
              volume: 458800000,
              width: 620,
            },
          },
          {
            itemId: 'EBD0100000093099',
            orientation: 'FRONT_UP',
            position: { x: 10920, y: 1200, z: 900 },
            rotatedCube: {
              height: 530,
              length: 1060,
              volume: 410114000,
              width: 730,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'FRONT_DOWN',
            position: { x: 6080, y: 1100, z: 1760 },
            rotatedCube: {
              height: 590,
              length: 590,
              volume: 313290000,
              width: 900,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'FRONT_DOWN',
            position: { x: 6640, y: 0, z: 1710 },
            rotatedCube: {
              height: 590,
              length: 590,
              volume: 313290000,
              width: 900,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'BOTTOM_UP',
            position: { x: 10980, y: 0, z: 1200 },
            rotatedCube: {
              height: 590,
              length: 900,
              volume: 313290000,
              width: 590,
            },
          },
          {
            itemId: 'EBD0100000095770',
            orientation: 'FRONT_DOWN',
            position: { x: 7230, y: 0, z: 1710 },
            rotatedCube: {
              height: 590,
              length: 590,
              volume: 313290000,
              width: 900,
            },
          },
          {
            itemId: 'EBD0100000093099',
            orientation: 'FRONT_UP',
            position: { x: 6670, y: 900, z: 1800 },
            rotatedCube: {
              height: 550,
              length: 680,
              volume: 269280000,
              width: 720,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 3000, y: 1200, z: 2200 },
            rotatedCube: {
              height: 420,
              length: 1280,
              volume: 268800000,
              width: 500,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 3000, y: 1700, z: 2200 },
            rotatedCube: {
              height: 420,
              length: 1280,
              volume: 268800000,
              width: 500,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 0, z: 2300 },
            rotatedCube: {
              height: 310,
              length: 930,
              volume: 268119000,
              width: 930,
            },
          },
          {
            itemId: 'EBD0100000086191',
            orientation: 'FRONT_UP',
            position: { x: 10920, y: 1930, z: 900 },
            rotatedCube: {
              height: 550,
              length: 880,
              volume: 203280000,
              width: 420,
            },
          },
          {
            itemId: 'EBD0100000086191',
            orientation: 'FRONT_UP',
            position: { x: 4260, y: 620, z: 2060 },
            rotatedCube: {
              height: 550,
              length: 880,
              volume: 203280000,
              width: 420,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'FRONT_UP',
            position: { x: 10070, y: 620, z: 1160 },
            rotatedCube: {
              height: 520,
              length: 650,
              volume: 192660000,
              width: 570,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_DOWN',
            position: { x: 10980, y: 590, z: 1200 },
            rotatedCube: {
              height: 400,
              length: 790,
              volume: 186440000,
              width: 590,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'SIDE_UP',
            position: { x: 930, y: 0, z: 2320 },
            rotatedCube: {
              height: 320,
              length: 660,
              volume: 185856000,
              width: 880,
            },
          },
          {
            itemId: 'EBD0100000085086',
            orientation: 'SIDE_UP',
            position: { x: 6670, y: 1620, z: 1800 },
            rotatedCube: {
              height: 530,
              length: 550,
              volume: 174900000,
              width: 600,
            },
          },
          {
            itemId: 'EBD0100000091870',
            orientation: 'FRONT_DOWN',
            position: { x: 1020, y: 1970, z: 1900 },
            rotatedCube: {
              height: 600,
              length: 800,
              volume: 168000000,
              width: 350,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'BOTTOM_UP',
            position: { x: 4430, y: 1100, z: 1300 },
            rotatedCube: {
              height: 270,
              length: 380,
              volume: 121068000,
              width: 1180,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 1820, y: 1970, z: 1900 },
            rotatedCube: {
              height: 270,
              length: 1180,
              volume: 121068000,
              width: 380,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'BOTTOM_UP',
            position: { x: 3000, y: 1200, z: 1900 },
            rotatedCube: {
              height: 270,
              length: 380,
              volume: 112860000,
              width: 1100,
            },
          },
          {
            itemId: 'EBD0100000091595',
            orientation: 'SIDE_UP',
            position: { x: 1590, y: 0, z: 2320 },
            rotatedCube: {
              height: 210,
              length: 580,
              volume: 87696000,
              width: 720,
            },
          },
          {
            itemId: 'EBD0100000083166',
            orientation: 'FRONT_UP',
            position: { x: 0, y: 930, z: 2300 },
            rotatedCube: {
              height: 380,
              length: 680,
              volume: 69768000,
              width: 270,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 1820, y: 1970, z: 2170 },
            rotatedCube: {
              height: 270,
              length: 680,
              volume: 69768000,
              width: 380,
            },
          },
          {
            itemId: 'EBD0100000085082',
            orientation: 'FRONT_DOWN',
            position: { x: 1590, y: 720, z: 2320 },
            rotatedCube: {
              height: 270,
              length: 680,
              volume: 69768000,
              width: 380,
            },
          },
        ],
        totalVolume: 56630547000,
        totalWeight: 69.0,
      },
    ],
};
const mockData2 = {
  singleContainerLoadingSolutions: [
    {
      container: {
        containerId: 'container',
        cube: {
          height: 2500,
          length: 11890,
          volume: 76351414272,
          width: 2320,
        },
        price: 3400.0,
        volume: 76351414272,
        weight: 30400.0,
      },
      placedItems: [{
        itemId: 'LEFT_1_1',
        orientation: 'FRONT_DOWN',
        position: { x: 0, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_1_2',
        orientation: 'FRONT_DOWN',
        position: { x: 0, y: 0, z: 920 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_1_3',
        orientation: 'FRONT_DOWN',
        position: { x: 0, y: 0, z: 1740 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_1_1',
        orientation: 'FRONT_DOWN',
        position: { x: 0, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_1_2',
        orientation: 'FRONT_DOWN',
        position: { x: 0, y: 1200, z: 1530 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_2_1',
        orientation: 'FRONT_DOWN',
        position: { x: 1300, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_2_2',
        orientation: 'FRONT_DOWN',
        position: { x: 1300, y: 0, z: 1490 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_2_1',
        orientation: 'FRONT_DOWN',
        position: { x: 1300, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_2_2',
        orientation: 'FRONT_DOWN',
        position: { x: 1300, y: 1200, z: 920 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_2_3',
        orientation: 'FRONT_DOWN',
        position: { x: 1300, y: 1200, z: 1480 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_3_1',
        orientation: 'FRONT_DOWN',
        position: { x: 2600, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_3_2',
        orientation: 'FRONT_DOWN',
        position: { x: 2600, y: 0, z: 1490 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_3_1',
        orientation: 'FRONT_DOWN',
        position: { x: 2600, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_3_2',
        orientation: 'FRONT_DOWN',
        position: { x: 2600, y: 1200, z: 1490 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_4_1',
        orientation: 'FRONT_DOWN',
        position: { x: 3900, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_4_2',
        orientation: 'FRONT_DOWN',
        position: { x: 3900, y: 0, z: 1490 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_4_1',
        orientation: 'FRONT_DOWN',
        position: { x: 3900, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_4_2',
        orientation: 'FRONT_DOWN',
        position: { x: 3900, y: 1200, z: 1380 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_5_1',
        orientation: 'FRONT_DOWN',
        position: { x: 5200, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_5_2',
        orientation: 'FRONT_DOWN',
        position: { x: 5200, y: 0, z: 1380 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_5_1',
        orientation: 'FRONT_DOWN',
        position: { x: 5200, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_5_2',
        orientation: 'FRONT_DOWN',
        position: { x: 5200, y: 1200, z: 1380 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_6_1',
        orientation: 'FRONT_DOWN',
        position: { x: 6500, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_6_2',
        orientation: 'FRONT_DOWN',
        position: { x: 6500, y: 0, z: 920 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_6_3',
        orientation: 'FRONT_DOWN',
        position: { x: 6500, y: 0, z: 1660 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_6_1',
        orientation: 'FRONT_DOWN',
        position: { x: 6500, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_6_2',
        orientation: 'FRONT_DOWN',
        position: { x: 6500, y: 1200, z: 1350 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_7_1',
        orientation: 'FRONT_DOWN',
        position: { x: 7800, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_7_2',
        orientation: 'FRONT_DOWN',
        position: { x: 7800, y: 0, z: 1530 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_7_1',
        orientation: 'FRONT_DOWN',
        position: { x: 7800, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_7_2',
        orientation: 'FRONT_DOWN',
        position: { x: 7800, y: 1200, z: 1350 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_8_1',
        orientation: 'FRONT_DOWN',
        position: { x: 9100, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_8_2',
        orientation: 'FRONT_DOWN',
        position: { x: 9100, y: 0, z: 920 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_8_1',
        orientation: 'FRONT_DOWN',
        position: { x: 9100, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_8_2',
        orientation: 'FRONT_DOWN',
        position: { x: 9100, y: 1200, z: 1160 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_9_1',
        orientation: 'FRONT_DOWN',
        position: { x: 10400, y: 0, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'LEFT_9_2',
        orientation: 'FRONT_DOWN',
        position: { x: 10400, y: 0, z: 1160 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_9_1',
        orientation: 'FRONT_DOWN',
        position: { x: 10400, y: 1200, z: 0 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      },{
        itemId: 'RIGHT_9_2',
        orientation: 'FRONT_DOWN',
        position: { x: 10400, y: 1200, z: 1090 },
        rotatedCube: {
          height: 200,
          length: 1300,
          volume: 1867662000,
          width: 1100,
        }
      }],
      placedCylinders: [{
        itemId: 'LEFT_1_1_1',
        color: new THREE.Color("blue"),
        itemId: 0,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_1_1_2',
        color: new THREE.Color("blue"),
        itemId: 0,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_1_1_3',
        color: new THREE.Color("blue"),
        itemId: 0,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_1_1_4',
        color: new THREE.Color("blue"),
        itemId: 0,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_1_1_5',
        color: new THREE.Color("blue"),
        itemId: 0,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_1_2_1',
        color: new THREE.Color("blue"),
        itemId: 1,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_1_2_2',
        color: new THREE.Color("blue"),
        itemId: 1,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_1_2_3',
        color: new THREE.Color("blue"),
        itemId: 1,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_1_2_4',
        color: new THREE.Color("blue"),
        itemId: 1,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_1_2_5',
        color: new THREE.Color("blue"),
        itemId: 1,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_1_2_6',
        color: new THREE.Color("blue"),
        itemId: 1,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_1_3_1',
        color: new THREE.Color("blue"),
        itemId: 2,
        position: { x: 650, y: 550, z: 0 },
        rotatedCube: {
          height: 420,
          diameter: 516,
        }
      },{
        itemId: 'RIGHT_1_1_1',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_2',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_3',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_4',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_5',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_6',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 270, y: 270, z: 640 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_7',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 270, y: 730, z: 640 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_8',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 680, y: 500, z: 640 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_9',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 1070, y: 270, z: 640 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_1_10',
        color: new THREE.Color("blue"),
        itemId: 3,
        position: { x: 1070, y: 730, z: 640 },
        rotatedCube: {
          height: 640,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_1_2_1',
        color: new THREE.Color("blue"),
        itemId: 34,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_1_2_2',
        color: new THREE.Color("blue"),
        itemId: 34,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 550,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_1_2_3',
        color: new THREE.Color("blue"),
        itemId: 34,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_1_2_4',
        color: new THREE.Color("blue"),
        itemId: 34,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_1_2_5',
        color: new THREE.Color("blue"),
        itemId: 34,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_1_2_6',
        color: new THREE.Color("blue"),
        itemId: 34,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_1',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_2',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_3',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_4',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_5',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_6',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_7',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 220, y: 220, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_8',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 220, y: 647, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_9',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 600, y: 401, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_10',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 600, y: 828, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_11',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 960, y: 220, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_1_12',
        color: new THREE.Color("blue"),
        itemId: 5,
        position: { x: 960, y: 647, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_2_1',
        color: new THREE.Color("blue"),
        itemId: 6,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_2_2',
        color: new THREE.Color("blue"),
        itemId: 6,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_2_3',
        color: new THREE.Color("blue"),
        itemId: 6,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_2_4',
        color: new THREE.Color("blue"),
        itemId: 6,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_2_5',
        color: new THREE.Color("blue"),
        itemId: 6,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_2_2_6',
        color: new THREE.Color("blue"),
        itemId: 6,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_2_1_1',
        color: new THREE.Color("blue"),
        itemId: 7,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_1_2',
        color: new THREE.Color("blue"),
        itemId: 7,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_1_3',
        color: new THREE.Color("blue"),
        itemId: 7,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_1_4',
        color: new THREE.Color("blue"),
        itemId: 7,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_1_5',
        color: new THREE.Color("blue"),
        itemId: 7,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 750,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_2_1',
        color: new THREE.Color("blue"),
        itemId: 8,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_2_2',
        color: new THREE.Color("blue"),
        itemId: 8,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_2_3',
        color: new THREE.Color("blue"),
        itemId: 8,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_2_4',
        color: new THREE.Color("blue"),
        itemId: 8,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_2_5',
        color: new THREE.Color("blue"),
        itemId: 8,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_2_3_1',
        color: new THREE.Color("blue"),
        itemId: 38,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_2_3_2',
        color: new THREE.Color("blue"),
        itemId: 38,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_2_3_3',
        color: new THREE.Color("blue"),
        itemId: 38,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_2_3_4',
        color: new THREE.Color("blue"),
        itemId: 38,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 1020,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_2_3_5',
        color: new THREE.Color("blue"),
        itemId: 38,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 1020,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_2_3_6',
        color: new THREE.Color("blue"),
        itemId: 38,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 1020,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_1',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_6',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_7',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 220, y: 220, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_8',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 220, y: 647, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_9',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 600, y: 401, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_10',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 600, y: 828, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_11',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 960, y: 220, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_1_12',
        color: new THREE.Color("blue"),
        itemId: 10,
        position: { x: 960, y: 647, z: 620 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_1',
        color: new THREE.Color("blue"),
        itemId: 11,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 11,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 11,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 11,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 11,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 11,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 630,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_3_1_1',
        color: new THREE.Color("blue"),
        itemId: 12,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 1290,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 12,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 1290,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 12,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 1290,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 12,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 1290,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 12,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 1290,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_2_1',
        color: new THREE.Color("blue"),
        itemId: 13,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 13,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 13,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 13,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 13,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_4_1_1',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_4_1_1',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 270, z: 285 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 730, z: 285 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 680, y: 500, z: 285 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 270, z: 285 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 730, z: 285 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_4_1_1',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 270, z: 570 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 730, z: 570 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 680, y: 500, z: 570 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 270, z: 570 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 730, z: 570 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_4_1_1',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 270, z: 855 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 270, y: 730, z: 855 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 680, y: 500, z: 855 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 270, z: 855 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 14,
        position: { x: 1070, y: 730, z: 855 },
        rotatedCube: {
          height: 285,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_4_2_1',
        color: new THREE.Color("blue"),
        itemId: 15,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 15,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 15,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 15,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 620,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 15,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 15,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_4_1_1',
        color: new THREE.Color("blue"),
        itemId: 16,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 16,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 16,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 16,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 16,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_4_2_1',
        color: new THREE.Color("blue"),
        itemId: 17,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 17,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 17,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 17,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 17,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_5_1_1',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 360,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_5_1_1',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 270, y: 270, z: 360 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 270, y: 730, z: 360 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 680, y: 500, z: 360 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 1070, y: 270, z: 360 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 1070, y: 730, z: 360 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_5_1_1',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 270, y: 270, z: 770 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 270, y: 730, z: 770 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 680, y: 500, z: 770 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 1070, y: 270, z: 770 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 18,
        position: { x: 1070, y: 730, z: 770 },
        rotatedCube: {
          height: 410,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_5_2_1',
        color: new THREE.Color("blue"),
        itemId: 19,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 19,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 19,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 19,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 19,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_5_1_1',
        color: new THREE.Color("blue"),
        itemId: 20,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 20,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 20,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 20,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 20,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 1180,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_5_2_1',
        color: new THREE.Color("blue"),
        itemId: 21,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 21,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 21,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 21,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 21,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_6_1_1',
        color: new THREE.Color("blue"),
        itemId: 22,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 22,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 22,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 22,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 22,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_6_2_1',
        color: new THREE.Color("blue"),
        itemId: 23,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 23,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 23,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 23,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 23,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 23,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_6_3_1',
        color: new THREE.Color("blue"),
        itemId: 24,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 420,
          diameter: 526,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 24,
        position: { x: 270, y: 796, z: 0 },
        rotatedCube: {
          height: 420,
          diameter: 526,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 24,
        position: { x: 796, y: 270, z: 0 },
        rotatedCube: {
          height: 420,
          diameter: 526,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 24,
        position: { x: 796, y: 796, z: 0 },
        rotatedCube: {
          height: 420,
          diameter: 526,
        }
      },{
        itemId: 'RIGHT_6_1_1',
        color: new THREE.Color("blue"),
        itemId: 25,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 25,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 25,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 25,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 25,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 25,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_6_2_1',
        color: new THREE.Color("blue"),
        itemId: 26,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 26,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 26,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 26,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 26,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_7_1_1',
        color: new THREE.Color("blue"),
        itemId: 27,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 1330,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 27,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 1330,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 27,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 1330,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 27,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 1330,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 27,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 1330,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_7_2_1',
        color: new THREE.Color("blue"),
        itemId: 28,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 28,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 540,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_7_2_1',
        color: new THREE.Color("blue"),
        itemId: 28,
        position: { x: 736, y: 258, z: 0 },
        rotatedCube: {
          height: 420,
          diameter: 516,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 28,
        position: { x: 736, y: 774, z: 0 },
        rotatedCube: {
          height: 420,
          diameter: 516,
        }
      },{
        itemId: 'RIGHT_7_1_1',
        color: new THREE.Color("blue"),
        itemId: 29,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 29,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 29,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 29,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 29,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 29,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 1150,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_7_2_1',
        color: new THREE.Color("blue"),
        itemId: 30,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 30,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 30,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 30,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 30,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_8_1_1',
        color: new THREE.Color("blue"),
        itemId: 31,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_2',
        color: new THREE.Color("blue"),
        itemId: 31,
        position: { x: 270, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_3',
        color: new THREE.Color("blue"),
        itemId: 31,
        position: { x: 680, y: 500, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_4',
        color: new THREE.Color("blue"),
        itemId: 31,
        position: { x: 1070, y: 270, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'RIGHT_3_1_5',
        color: new THREE.Color("blue"),
        itemId: 31,
        position: { x: 1070, y: 730, z: 0 },
        rotatedCube: {
          height: 720,
          diameter: 478,
        }
      },{
        itemId: 'LEFT_8_2_1',
        color: new THREE.Color("blue"),
        itemId: 32,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 1020,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 32,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 1020,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 32,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 32,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 32,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 32,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_8_1_1',
        color: new THREE.Color("blue"),
        itemId: 33,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 33,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 33,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 33,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 33,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 33,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_8_2_1',
        color: new THREE.Color("blue"),
        itemId: 4,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 4,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 4,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 4,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 4,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 4,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_9_1_1',
        color: new THREE.Color("blue"),
        itemId: 35,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 35,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 35,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 35,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 35,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 35,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 960,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_9_2_1',
        color: new THREE.Color("blue"),
        itemId: 36,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 36,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 36,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 730,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 36,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 36,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 36,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 660,
          diameter: 427,
        }
      },{
        itemId: 'RIGHT_9_1_1',
        color: new THREE.Color("blue"),
        itemId: 37,
        position: { x: 270, y: 270, z: 0 },
        rotatedCube: {
          height: 890,
          diameter: 526,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 37,
        position: { x: 270, y: 796, z: 0 },
        rotatedCube: {
          height: 890,
          diameter: 526,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 37,
        position: { x: 796, y: 270, z: 0 },
        rotatedCube: {
          height: 890,
          diameter: 526,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 37,
        position: { x: 796, y: 796, z: 0 },
        rotatedCube: {
          height: 890,
          diameter: 526,
        }
      },{
        itemId: 'RIGHT_9_2_1',
        color: new THREE.Color("blue"),
        itemId: 9,
        position: { x: 220, y: 220, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_2',
        color: new THREE.Color("blue"),
        itemId: 9,
        position: { x: 220, y: 647, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_3',
        color: new THREE.Color("blue"),
        itemId: 9,
        position: { x: 600, y: 401, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_4',
        color: new THREE.Color("blue"),
        itemId: 9,
        position: { x: 600, y: 828, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_5',
        color: new THREE.Color("blue"),
        itemId: 9,
        position: { x: 960, y: 220, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      },{
        itemId: 'LEFT_3_2_6',
        color: new THREE.Color("blue"),
        itemId: 9,
        position: { x: 960, y: 647, z: 0 },
        rotatedCube: {
          height: 760,
          diameter: 427,
        }
      }],
      totalVolume: 56630547000,
      totalWeight: 69.0,
    },
  ],
};

let cartonWidth;
let cartonHeight;
let cartonLength;
let detailIndex = 0;
// let angle = 0;
let intersections;
let intersected;
const defaults = {
    result: [],
    detailList: [],
    dataList: [],
    detailNum: 0,
    cartonNum: 0,
    taskNum: 0,
    cartonList: [],
};
let HEIGHT;
let WIDTH;
let boxArr = [];

// 创建场景
const scene = new THREE.Scene();
// 场景颜色
// scene.background = new THREE.Color(0x999999);
scene.background = new THREE.Color("#E0E0E0");

// 创建相机 参数：（视角， 宽高比，近平面，远平面）
const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    1,
    99999
);
// 调整相机位置
camera.position.set(12000, 0, 0);
camera.up.x = 0;
camera.up.y = 1;
camera.up.z = 0;
camera.lookAt({
    x: 0,
    y: 0,
    z: 200,
});
scene.add(camera);

// 初始化网格
const grid = new THREE.GridHelper(15000, 20, 0x333333, 0x333333);

// 初始化渲染器并设置场景大小
const renderer = new THREE.WebGLRenderer({
    antialias: true, // 开启锯齿
    alpha: true, // 透明度
});
renderer.setSize( window.innerWidth, window.innerHeight );
//添加到相应元素中
document.body.appendChild( renderer.domElement );

// 初始化轨道控制器
const controls = new OrbitControls(camera, renderer.domElement);
// 控制器阻尼
controls.enableDamping = true;
// 动态阻尼系数
controls.dampingFactor = 0.1;
// 旋转中心点
controls.target.set(0, 0, 0);

// 三维坐标轴
const axesHelper = new THREE.AxesHelper(5000);
scene.add( axesHelper );

// 选中子级盒子
const mouse = new THREE.Vector3();
// 射线
const raycaster = new THREE.Raycaster();
window.addEventListener("click", (event) => {
	// 设置鼠标向量的xy值（归一化，使xy坐标的范围在-1到1之间）
	mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
	mouse.y = -((event.clientY / window.innerHeight) * 2 - 1);
	// 通过摄像机和鼠标位置更新射线
	raycaster.setFromCamera(mouse, camera);
	// 计算物体和射线的焦点
	intersections = raycaster.intersectObjects(boxArr);
	// 
	if(intersections.length > 0) {
        intersected = intersections[0].object;
        console.log(intersected);
	}
});

// 获取详细数据(获取货物数据)
function getInfoDetail() {
    const res = { status: 200, data: [], success: true };
    // console.log(mockData.singleContainerLoadingSolutions);
    res.data = mockData2.singleContainerLoadingSolutions;
    defaults.result = res;
    defaults.detailList = [];

    // 初始装货箱信息
    const { width, length, height } = res.data[0].container.cube;
    initBox(width, height, length, res.data[0].container);

    // 单个详情
    const placedItemsArr = res.data[0].placedItems;
    detailIndex = defaults.detailNum = placedItemsArr.length;

    const placedCylinderArr = res.data[0].placedCylinders;

    // 渲染单个子级盒子
    boxArr = [];
    for (let i = 0; i < defaults.detailNum; i++) {
        const detail = placedItemsArr[i];
        defaults.detailList.push(
            initObject(
                detail.rotatedCube.width,
                detail.rotatedCube.height,
                detail.rotatedCube.length,
                detail.position.x,
                detail.position.y,
                detail.position.z,
                // i
                detail.itemId
            )
        );
    }

    for (let i = 0; i < placedCylinderArr.length; i++) {
      const detail = placedCylinderArr[i];
      defaults.detailList.push(
          initCylinder(
              detail.rotatedCube.diameter,
              detail.rotatedCube.height,
              detail.position.x,
              detail.position.y,
              detail.position.z,
              detail.color,
              detail.itemId
          )
      );
  }
};
// 初始化纸箱(车箱)
function initBox(xLen, yLen, zLen, context) {
    // setContainerContext(context);
    cartonWidth = xLen;
    cartonHeight = yLen;
    cartonLength = zLen;
    // 声明几何体
    const geometry = new THREE.BoxGeometry(xLen, yLen, zLen);
    // 声明材质;
    const edges = new THREE.EdgesGeometry(geometry);
    // 几何体+ 材质 = 物体
    const containerBox = new THREE.LineSegments(edges);
    containerBox.material.color = new THREE.Color(0x000000);
    containerBox.position.set(0, 0, 0);
    // 将物体添加到场景中
    scene.add(containerBox);
    // 添加网格
    grid.position.y = -(cartonHeight / 2) - cartonHeight / 8;
    // scene.add(grid);
    return containerBox;
};
// 设置每个子级盒子（这里创建了车箱中的货物几何体，其中对其顶面通过getTextCanvas单独设置了材质，还再货物外面套了一个相同大小的边缘几何体）
function initObject(width, height, length, x, y, z, index) {
    const mesh = new THREE.Object3D();
    const geometry = new THREE.BoxGeometry(width, height, length);
    // 设置随机颜色
    const color = new THREE.Color(0xff794204);
    // 设置子级盒子材质
    const material = [];
    for (let j = 0; j < geometry.groups.length; j++) {
        const mats = new THREE.MeshBasicMaterial({
            color,
            transparent: true,
            opacity: 0.8,
        });
        material.push(mats);
    }

    // console.log(
    //   '宽:',
    //   width,
    //   '高:',
    //   height,
    //   '长:',
    //   length,
    //   '体积:',
    //   width * height * length,
    // );

    // 上下面
    // material[2].map = new THREE.CanvasTexture(
    //     getTextCanvas(width, height, length, index)
    // );

    // 几何体 + 材质 = 物体
    const cube = new THREE.Mesh(geometry, material);

    // !!! 添加额外物体属性
    cube.itemId = index;

    // 3D模型添加 材质和几何体
    mesh.add(cube);
    // 设置子级盒子边框
    const wideFrame = new THREE.BoxGeometry(width, height, length);
    const materialBorder = new THREE.EdgesGeometry(wideFrame);
    const lineFrame = new THREE.LineSegments(
        materialBorder,
        new THREE.LineBasicMaterial({ color: 0xff131313 })
    );
    mesh.add(lineFrame);
    // 装箱复位
    mesh.position.set(
        y + width / 2 - cartonWidth / 2,
        z + height / 2 - cartonHeight / 2,
        x + length / 2 - cartonLength / 2,
        'XYZ'
    );
    // mesh.object.itemId = index;
    scene.add(mesh);
    boxArr.push(cube);
    return mesh;
};
function initCylinder(diameter, height, x, y, z, color, index) {
  const mesh = new THREE.Object3D();
    // 创建圆柱体几何体
  const geometry = new THREE.CylinderGeometry(diameter / 2, diameter / 2, height, 32);

    // 设置子级盒子材质
  const material = new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: 0.8,
  });
    // 
  const cylinder = new THREE.Mesh(geometry, material);

  const wideFrame = new THREE.CylinderGeometry(diameter / 2, diameter / 2, height, 32);
  const materialBorder = new THREE.EdgesGeometry(wideFrame);
  const lineFrame = new THREE.LineSegments(
      materialBorder,
      new THREE.LineBasicMaterial({ color: 0xff131313 })
  );
  cylinder.add(lineFrame);

  const res = defaults.result;
  const itemPositionLength = res.data[0].placedItems[index].position.x; 
  const itemPositionWidth = res.data[0].placedItems[index].position.y;
  const itemPositionHeight = res.data[0].placedItems[index].position.z;
  // console.log(itemPositionLength, itemPositionHeight, itemPositionWidth);

  cylinder.position.set(
      y +  - cartonWidth / 2 + itemPositionWidth,
      z + 200 + height/2 - cartonHeight / 2 + itemPositionHeight,
      x +  - cartonLength / 2 + itemPositionLength,
      'XYZ'
  );

  scene.add(cylinder);
  return cylinder;
};

getInfoDetail()

//渲染函数
function animate() {
	//这里是动画函数，会不断调用，刷新帧(拖动、缩放也需要)
	requestAnimationFrame( animate );

	controls.update();
	//渲染
	renderer.render( scene, camera );
}
animate();

// 监听窗口变化
window.addEventListener("resize", () => {
	// 重置渲染器宽高比
	renderer.setSize(window.innerWidth, window.innerHeight);
	// 重置相机宽高比
	camera.aspect = window.innerWidth / window.innerHeight;
	// 更新相机投影矩阵
	camera.updateProjectionMatrix();
})
