# Changelog

## [0.4.0](https://github.com/westonplatter/ngv_reports_ibkr/compare/v0.3.0...v0.4.0) (2026-02-05)


### ⚠ BREAKING CHANGES

* Discord integration is no longer supported.

### Features

* created unified data framework concept ([#49](https://github.com/westonplatter/ngv_reports_ibkr/issues/49)) ([78d21ec](https://github.com/westonplatter/ngv_reports_ibkr/commit/78d21ec2b52da027b366c57118fcfcf8fb3a9d59))
* remove deprecated Discord integration ([#44](https://github.com/westonplatter/ngv_reports_ibkr/issues/44)) ([53f0782](https://github.com/westonplatter/ngv_reports_ibkr/commit/53f0782df527379c336fc7e0679d5f377d9c0c4b))


### Documentation

* add uv direct install instructions to README ([#46](https://github.com/westonplatter/ngv_reports_ibkr/issues/46)) ([841bf86](https://github.com/westonplatter/ngv_reports_ibkr/commit/841bf86b54b93a443fbe46ac8712986358b40756))
* Update audit fields. Set audit fields = yes, break out by day = yes ([#43](https://github.com/westonplatter/ngv_reports_ibkr/issues/43)) ([3c3d140](https://github.com/westonplatter/ngv_reports_ibkr/commit/3c3d140ebff0b2bcd1c19ca0565a4058e68b86f0))
* update Time Format to include Timezone in README ([#41](https://github.com/westonplatter/ngv_reports_ibkr/issues/41)) ([49b5f53](https://github.com/westonplatter/ngv_reports_ibkr/commit/49b5f53f6b2d7b356140ab75e9d19e1f70dfb2bd))


### Miscellaneous Chores

* **deps:** upgrade pandera to 0.29.0, add TWS trades schema tests ([#45](https://github.com/westonplatter/ngv_reports_ibkr/issues/45)) ([a36de2d](https://github.com/westonplatter/ngv_reports_ibkr/commit/a36de2dcd66e8d7341562615a8b3d5933ae1bdec))
* update rp configs ([#50](https://github.com/westonplatter/ngv_reports_ibkr/issues/50)) ([12470c4](https://github.com/westonplatter/ngv_reports_ibkr/commit/12470c45c2647488bdc6d51c97249a6ef3f3c886))

## [0.3.0](https://github.com/westonplatter/ngv_reports_ibkr/compare/v0.2.0...v0.3.0) (2026-01-30)


### Features

* add pull request template ([#26](https://github.com/westonplatter/ngv_reports_ibkr/issues/26)) ([a3ce3a0](https://github.com/westonplatter/ngv_reports_ibkr/commit/a3ce3a0e8b64e67216126824240509196b63b8c8))
* prepwork for unified TWS Trades + Flex Query Trades df ([#38](https://github.com/westonplatter/ngv_reports_ibkr/issues/38)) ([bae0e7c](https://github.com/westonplatter/ngv_reports_ibkr/commit/bae0e7c6c009c025bcbd044ff2fed592ded630b5))
* **realtime:** create basic structure for reporting real time IBKR TWS trades ([#32](https://github.com/westonplatter/ngv_reports_ibkr/issues/32)) ([b2a1ac6](https://github.com/westonplatter/ngv_reports_ibkr/commit/b2a1ac65d78454e9b8ef7bdaf778575e1039c167))
* **schemas:** add pandera schema for trades by account ([#33](https://github.com/westonplatter/ngv_reports_ibkr/issues/33)) ([6183255](https://github.com/westonplatter/ngv_reports_ibkr/commit/61832559ff5e23585354d1bec0a92b66b3266c63))
* setup rp ([#40](https://github.com/westonplatter/ngv_reports_ibkr/issues/40)) ([6738d3f](https://github.com/westonplatter/ngv_reports_ibkr/commit/6738d3fae7a9ad3d7081ebb86ec9e945c602e0cc))


### Bug Fixes

* **gha:** make it work with the uv group ([#34](https://github.com/westonplatter/ngv_reports_ibkr/issues/34)) ([40611c3](https://github.com/westonplatter/ngv_reports_ibkr/commit/40611c39f5e76a430052dad8b102c2dd9925729f))


### Documentation

* review and fix documentation issues ([#31](https://github.com/westonplatter/ngv_reports_ibkr/issues/31)) ([453bb81](https://github.com/westonplatter/ngv_reports_ibkr/commit/453bb8117242ebae864b39d45e824db337863ace))
* update README ([#35](https://github.com/westonplatter/ngv_reports_ibkr/issues/35)) ([032c40c](https://github.com/westonplatter/ngv_reports_ibkr/commit/032c40cbf29fcdc38d776c60dc8ff9549680ed47))


### Miscellaneous Chores

* clean up. remove older setup.py files ([2b6c1dd](https://github.com/westonplatter/ngv_reports_ibkr/commit/2b6c1dd2557b63d25f8e77786fa8d872599e2d45))

## [0.2.0](https://github.com/westonplatter/ngv_reports_ibkr/compare/0.1.1...v0.2.0) (2025-11-14)


### Features

* add 3.11-3.14 versions ([#16](https://github.com/westonplatter/ngv_reports_ibkr/issues/16)) ([5c0735e](https://github.com/westonplatter/ngv_reports_ibkr/commit/5c0735ecd33cb3bcb8b539aecfc226e4c8c6853a))
* switch to Python-specific release-please workflow ([#22](https://github.com/westonplatter/ngv_reports_ibkr/issues/22)) ([5e6108c](https://github.com/westonplatter/ngv_reports_ibkr/commit/5e6108c9b46a232381bc7fa8b9d94ca105e75c0d))
* update to &gt;= 3.9 ([#19](https://github.com/westonplatter/ngv_reports_ibkr/issues/19)) ([cb4ea15](https://github.com/westonplatter/ngv_reports_ibkr/commit/cb4ea1509119349c36f7e45d8f423ba26dc54a6b))


### Bug Fixes

* update docs workflow to use ubuntu-latest runner ([#21](https://github.com/westonplatter/ngv_reports_ibkr/issues/21)) ([cd38570](https://github.com/westonplatter/ngv_reports_ibkr/commit/cd38570f2fd5f6f61c1b14ae4af1e8322f5383c0))
