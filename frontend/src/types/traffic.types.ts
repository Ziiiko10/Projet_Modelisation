import { Position } from './vehicle.types';

export interface TrafficLightPhase {
  duration: number;
  state: string;
  minDuration?: number;
  maxDuration?: number;
}

export interface TrafficLight {
  id: string;
  position: Position;
  state: string;
  currentPhase: number;
  phases: TrafficLightPhase[];
  remainingDuration?: number;
}

export interface TrafficLightUpdate {
  id: string;
  state: string;
  currentPhase: number;
  remainingDuration?: number;
  timestamp: number;
}

export interface RoadSegment {
  id: string;
  from: string;
  to: string;
  length: number;
  lanes: number;
  speedLimit: number;
  coordinates: Position[];
  congestionLevel?: 'free' | 'normal' | 'congested';
}

export interface Junction {
  id: string;
  position: Position;
  type: string;
  connectedRoads: string[];
}
