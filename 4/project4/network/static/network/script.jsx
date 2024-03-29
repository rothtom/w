import { func } from 'prop-types';
import * as index from './index';
import { Profiler } from 'react';

if (document.readyState !== 'loading') {
    init();
} else {
    document.addEventListener('DOMContentLoaded', function () {
        init();
    });
}

function init() {
    index.body();
}