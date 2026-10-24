import React from 'react';

export type ExtrapolateType = 'clamp' | 'extend' | 'identity';

export interface InterpolateOptions {
  extrapolateLeft?: ExtrapolateType;
  extrapolateRight?: ExtrapolateType;
}

export interface InterpolateProps {
  input: number;
  inputRange: number[];
  outputRange: number[];
  extrapolate?: ExtrapolateType | InterpolateOptions;
}

export const interpolate = (
  input: number,
  inputRange: number[],
  outputRange: number[],
  extrapolate: ExtrapolateType | InterpolateOptions = 'clamp'
): number => {
  const leftRule: ExtrapolateType = typeof extrapolate === 'object'
    ? (extrapolate.extrapolateLeft ?? 'clamp')
    : extrapolate;
  const rightRule: ExtrapolateType = typeof extrapolate === 'object'
    ? (extrapolate.extrapolateRight ?? 'clamp')
    : extrapolate;
  if (inputRange.length !== outputRange.length) {
    throw new Error('inputRange and outputRange must have same length');
  }
  if (inputRange.length < 2) {
    throw new Error('inputRange and outputRange must have at least 2 points');
  }

  // Lower bound check
  if (input <= inputRange[0]) {
    if (leftRule === 'clamp') return outputRange[0];
    if (leftRule === 'identity') return input;
  }

  // Upper bound check
  if (input >= inputRange[inputRange.length - 1]) {
    if (rightRule === 'clamp') return outputRange[outputRange.length - 1];
    if (rightRule === 'identity') return input;
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
