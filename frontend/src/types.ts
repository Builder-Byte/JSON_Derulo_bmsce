export interface Patient {
  id: string;
  riskScore: number;
  trend: number[];
  primaryTrigger: string;
  csi: number;
  protocol: string;
  status: 'critical' | 'elevated' | 'normal';
}

export interface Alert {
  id: string;
  type: 'critical' | 'elevated';
  time: string;
  subjectId: string;
  title: string;
  message: string;
}
