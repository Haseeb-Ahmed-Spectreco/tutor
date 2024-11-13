import React from 'react';

import { getConfig } from '@edx/frontend-platform';
import { useIntl } from '@edx/frontend-platform/i18n';
import { Hyperlink, Image } from '@openedx/paragon';
import classNames from 'classnames';

import messages from './messages';

const LargeLayout = () => {
  const { formatMessage } = useIntl();

  return (
    <div className="w-50 d-flex">
      <div className="col-md-9" style={{backgroundColor: "#bc18234a"}}>
        <Hyperlink destination={getConfig().MARKETING_SITE_BASE_URL}>
        </Hyperlink>
        <div className="min-vh-100 d-flex align-items-center">
          <div className={classNames({ 'large-yellow-line mr-n4.5': getConfig().SITE_NAME === 'edX' })} />
          <h1
            className={classNames(
              'display-2 text-white mw-xs',
              { 'ml-6': getConfig().SITE_NAME !== 'edX' },
            )}
          >
            {formatMessage(messages['start.learning'])}
            <div  style={{color: "#bc1823"}}>
              {formatMessage(messages['with.site.name'], { siteName: getConfig().SITE_NAME })}
            </div>
          </h1>
        </div>
      </div>
      <div className="col-md-3 bg-white p-0">
        <svg className=" w-100 h-100 "  preserveAspectRatio="xMaxYMin meet">
          <g transform="skewX(171.6)">
            <rect x="0" y="0" height="100%" width="100%" fill="#bc18234a" />
          </g>
        </svg>
      </div>
    </div>
  );
};

export default LargeLayout;
