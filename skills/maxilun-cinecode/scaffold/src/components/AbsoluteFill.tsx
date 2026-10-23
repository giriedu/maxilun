import React from 'react';

interface AbsoluteFillProps {
  style?: React.CSSProperties;
  children: React.ReactNode;
}

export const AbsoluteFill: React.FC<AbsoluteFillProps> = ({ style, children }) => {
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        overflow: 'hidden',
        ...style,
      }}
    >
      {children}
    </div>
  );
};
