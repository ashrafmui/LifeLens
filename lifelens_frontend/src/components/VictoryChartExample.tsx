// components/VictoryChartExample.tsx

"use client";

import React from 'react';
import { VictoryBar, VictoryChart, VictoryAxis, VictoryTheme } from 'victory';

const data = [
  { quarter: 1, earnings: 13000 },
  { quarter: 2, earnings: 16500 },
  { quarter: 3, earnings: 14250 },
  { quarter: 4, earnings: 19000 },
];

const VictoryChartExample: React.FC = () => {
  return (
    <VictoryChart theme={VictoryTheme.material} domainPadding={20}>
      <VictoryAxis
        tickValues={[1, 2, 3, 4]}
        tickFormat={['Total Sleep', 'Deep Sleep', 'Light Sleep', 'Quarter 4']}
      />
      <VictoryAxis dependentAxis tickFormat={(x) => `$${x / 1000}k`} />
      <VictoryBar data={data} x="quarter" y="earnings" />
    </VictoryChart>
  );
};



export default VictoryChartExample;
