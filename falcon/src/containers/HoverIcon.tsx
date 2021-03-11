import { Icon } from '@material-ui/core';
import styled from 'styled-components';
import React from 'react';
import { styles } from '../styles/styleguide';

const Hover = styled.div`
  transition: color ${styles.transitionParams};
  cursor: pointer;
  &:hover {
    color: ${styles.colorG1};
  }
`;
interface Props {
  icon: string;
  size?: 'large' | 'small';
}
export const HoverIcon = ({ icon, size }: Props) => {
  return (
    <Hover>
      <Icon fontSize={size}>{icon}</Icon>
    </Hover>
  );
};
