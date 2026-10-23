import React from 'react';

interface InterpolateProps {
  input: number;
  inputRange: number[];
  outputRange: number[];
  extrapolate?: 'clamp' | 'extend' | 'identity';
}

export const interpolate = (
  input: number,
  inputRange: number[],
  outputRange: number[],
  extrapolate: 'clamp' | 'extend' | 'identity' = 'clamp'
): number => {
  if (inputRange.length !== outputRange.length) {
    throw new Error('inputRange and outputRange must have same length');
  }
  if (inputRange.length < 2) {
    throw new Error('inputRange and outputRange must have at least 2 points');
  }

  // Lower bound check
  if (input <= inputRange[0]) {
    if (extrapolate === 'clamp') return outputRange[0];
    if (extrapolate === 'identity') return input;
  }

  // Upper bound check
  if (input >= inputRange[inputRange.length - 1]) {
    if (extrapolate === 'clamp') return outputRange[outputRange.length - 1];
    if (extrapolate === 'identity') return input;
  }

  // Find segment
  let i = 0;
  for (; i < inputRange.length - 1; i++) {
    if (input <= inputRange[i + 1]) break;
  }
  if (i >= inputRange.length - 1) {
    i = inputRange.length - 2;
  }

  const inputMin = inputRange[i];
  const inputMax = inputRange[i + 1];
  const outputMin = outputRange[i];
  const outputMax = outputRange[i + 1];

  if (inputMax === inputMin) {
    return outputMin;
  }

  const progress = (input - inputMin) / (inputMax - inputMin);
  return outputMin + progress * (outputMax - outputMin);
};
