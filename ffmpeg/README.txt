FFmpeg 64-bit static Windows build from www.gyan.dev

Version: 2024-05-27-git-01c7f68f7a-full_build-www.gyan.dev

License: GPL v3

Source Code: https://github.com/FFmpeg/FFmpeg/commit/01c7f68f7a

External Assets
frei0r plugins:   https://www.gyan.dev/ffmpeg/builds/ffmpeg-frei0r-plugins
lensfun database: https://www.gyan.dev/ffmpeg/builds/ffmpeg-lensfun-db

git-full build configuration: 

ARCH                      x86 (generic)
big-endian                no
runtime cpu detection     yes
standalone assembly       yes
x86 assembler             nasm
MMX enabled               yes
MMXEXT enabled            yes
3DNow! enabled            yes
3DNow! extended enabled   yes
SSE enabled               yes
SSSE3 enabled             yes
AESNI enabled             yes
AVX enabled               yes
AVX2 enabled              yes
AVX-512 enabled           yes
AVX-512ICL enabled        yes
XOP enabled               yes
FMA3 enabled              yes
FMA4 enabled              yes
i686 features enabled     yes
CMOV is fast              yes
EBX available             yes
EBP available             yes
debug symbols             yes
strip symbols             yes
optimize for size         no
optimizations             yes
static                    yes
shared                    no
postprocessing support    yes
network support           yes
threading support         pthreads
safe bitstream reader     yes
texi2html enabled         no
perl enabled              yes
pod2man enabled           yes
makeinfo enabled          yes
makeinfo supports HTML    yes
xmllint enabled           yes

External libraries:
avisynth                libgsm                  libsvtav1
bzlib                   libharfbuzz             libtheora
chromaprint             libilbc                 libtwolame
frei0r                  libjxl                  libuavs3d
gmp                     liblensfun              libvidstab
gnutls                  libmodplug              libvmaf
iconv                   libmp3lame              libvo_amrwbenc
ladspa                  libmysofa               libvorbis
libaom                  libopencore_amrnb       libvpx
libaribb24              libopencore_amrwb       libwebp
libaribcaption          libopenjpeg             libx264
libass                  libopenmpt              libx265
libbluray               libopus                 libxavs2
libbs2b                 libplacebo              libxevd
libcaca                 librav1e                libxeve
libcdio                 librist                 libxml2
libcodec2               librubberband           libxvid
libdav1d                libshaderc              libzimg
libdavs2                libshine                libzmq
libflite                libsnappy               libzvbi
libfontconfig           libsoxr                 lzma
libfreetype             libspeex                mediafoundation
libfribidi              libsrt                  sdl2
libgme                  libssh                  zlib

External libraries providing hardware acceleration:
amf                     d3d12va                 nvdec
cuda                    dxva2                   nvenc
cuda_llvm               ffnvcodec               opencl
cuvid                   libmfx                  vaapi
d3d11va                 libvpl                  vulkan

Libraries:
avcodec                 avformat                swresample
avdevice                avutil                  swscale
avfilter                postproc

Programs:
ffmpeg                  ffplay                  ffprobe

Enabled decoders:
aac                     g2m                     pcm_vidc
aac_fixed               g723_1                  pcx
aac_latm                g729                    pdv
aasc                    gdv                     pfm
ac3                     gem                     pgm
ac3_fixed               gif                     pgmyuv
acelp_kelvin            gremlin_dpcm            pgssub
adpcm_4xm               gsm                     pgx
adpcm_adx               gsm_ms                  phm
adpcm_afc               h261                    photocd
adpcm_agm               h263                    pictor
adpcm_aica              h263i                   pixlet
adpcm_argo              h263p                   pjs
adpcm_ct                h264                    png
adpcm_dtk               h264_cuvid              ppm
adpcm_ea                h264_qsv                prores
adpcm_ea_maxis_xa       hap                     prosumer
adpcm_ea_r1             hca                     psd
adpcm_ea_r2             hcom                    ptx
adpcm_ea_r3             hdr                     qcelp
adpcm_ea_xas            hevc                    qdm2
adpcm_g722              hevc_cuvid              qdmc
adpcm_g726              hevc_qsv                qdraw
adpcm_g726le            hnm4_video              qoa
adpcm_ima_acorn         hq_hqa                  qoi
adpcm_ima_alp           hqx                     qpeg
adpcm_ima_amv           huffyuv                 qtrle
adpcm_ima_apc           hymt                    r10k
adpcm_ima_apm           iac                     r210
adpcm_ima_cunning       idcin                   ra_144
adpcm_ima_dat4          idf                     ra_288
adpcm_ima_dk3           iff_ilbm                ralf
adpcm_ima_dk4           ilbc                    rasc
adpcm_ima_ea_eacs       imc                     rawvideo
adpcm_ima_ea_sead       imm4                    realtext
adpcm_ima_iss           imm5                    rka
adpcm_ima_moflex        indeo2                  rl2
adpcm_ima_mtf           indeo3                  roq
adpcm_ima_oki           indeo4                  roq_dpcm
adpcm_ima_qt            indeo5                  rpza
adpcm_ima_rad           interplay_acm           rscc
adpcm_ima_smjpeg        interplay_dpcm          rtv1
adpcm_ima_ssi           interplay_video         rv10
adpcm_ima_wav           ipu                     rv20
adpcm_ima_ws            jacosub                 rv30
adpcm_ms                jpeg2000                rv40
adpcm_mtaf              jpegls                  s302m
adpcm_psx               jv                      sami
adpcm_sbpro_2           kgv1                    sanm
adpcm_sbpro_3           kmvc                    sbc
adpcm_sbpro_4           lagarith                scpr
adpcm_swf               lead                    screenpresso
adpcm_thp               libaom_av1              sdx2_dpcm
adpcm_thp_le            libaribb24              sga
adpcm_vima              libaribcaption          sgi
adpcm_xa                libcodec2               sgirle
adpcm_xmd               libdav1d                sheervideo
adpcm_yamaha            libdavs2                shorten
adpcm_zork              libgsm                  simbiosis_imx
agm                     libgsm_ms               sipr
aic                     libilbc                 siren
alac                    libjxl                  smackaud
alias_pix               libopencore_amrnb       smacker
als                     libopencore_amrwb       smc
amrnb                   libopus                 smvjpeg
amrwb                   libspeex                snow
amv                     libuavs3d               sol_dpcm
anm                     libvorbis               sonic
ansi                    libvpx_vp8              sp5x
anull                   libvpx_vp9              speedhq
apac                    libxevd                 speex
ape                     libzvbi_teletext        srgc
apng                    loco                    srt
aptx                    lscr                    ssa
aptx_hd                 m101                    stl
arbc                    mace3                   subrip
argo                    mace6                   subviewer
ass                     magicyuv                subviewer1
asv1                    mdec                    sunrast
asv2                    media100                svq1
atrac1                  metasound               svq3
atrac3                  microdvd                tak
atrac3al                mimic                   targa
atrac3p                 misc4                   targa_y216
atrac3pal               mjpeg                   tdsc
atrac9                  mjpeg_cuvid             text
aura                    mjpeg_qsv               theora
aura2                   mjpegb                  thp
av1                     mlp                     tiertexseqvideo
av1_cuvid               mmvideo                 tiff
av1_qsv                 mobiclip                tmv
avrn                    motionpixels            truehd
avrp                    movtext                 truemotion1
avs                     mp1                     truemotion2
avui                    mp1float                truemotion2rt
bethsoftvid             mp2                     truespeech
bfi                     mp2float                tscc
bink                    mp3                     tscc2
binkaudio_dct           mp3adu                  tta
binkaudio_rdft          mp3adufloat             twinvq
bintext                 mp3float                txd
bitpacked               mp3on4                  ulti
bmp                     mp3on4float             utvideo
bmv_audio               mpc7                    v210
bmv_video               mpc8                    v210x
bonk                    mpeg1_cuvid             v308
brender_pix             mpeg1video              v408
c93                     mpeg2_cuvid             v410
cavs                    mpeg2_qsv               vb
cbd2_dpcm               mpeg2video              vble
ccaption                mpeg4                   vbn
cdgraphics              mpeg4_cuvid             vc1
cdtoons                 mpegvideo               vc1_cuvid
cdxl                    mpl2                    vc1_qsv
cfhd                    msa1                    vc1image
cinepak                 mscc                    vcr1
clearvideo              msmpeg4v1               vmdaudio
cljr                    msmpeg4v2               vmdvideo
cllc                    msmpeg4v3               vmix
comfortnoise            msnsiren                vmnc
cook                    msp2                    vnull
cpia                    msrle                   vorbis
cri                     mss1                    vp3
cscd                    mss2                    vp4
cyuv                    msvideo1                vp5
dca                     mszh                    vp6
dds                     mts2                    vp6a
derf_dpcm               mv30                    vp6f
dfa                     mvc1                    vp7
dfpwm                   mvc2                    vp8
dirac                   mvdv                    vp8_cuvid
dnxhd                   mvha                    vp8_qsv
dolby_e                 mwsc                    vp9
dpx                     mxpeg                   vp9_cuvid
dsd_lsbf                nellymoser              vp9_qsv
dsd_lsbf_planar         notchlc                 vplayer
dsd_msbf                nuv                     vqa
dsd_msbf_planar         on2avc                  vqc
dsicinaudio             opus                    vvc
dsicinvideo             osq                     wady_dpcm
dss_sp                  paf_audio               wavarc
dst                     paf_video               wavpack
dvaudio                 pam                     wbmp
dvbsub                  pbm                     wcmv
dvdsub                  pcm_alaw                webp
dvvideo                 pcm_bluray              webvtt
dxa                     pcm_dvd                 wmalossless
dxtory                  pcm_f16le               wmapro
dxv                     pcm_f24le               wmav1
eac3                    pcm_f32be               wmav2
eacmv                   pcm_f32le               wmavoice
eamad                   pcm_f64be               wmv1
eatgq                   pcm_f64le               wmv2
eatgv                   pcm_lxf                 wmv3
eatqi                   pcm_mulaw               wmv3image
eightbps                pcm_s16be               wnv1
eightsvx_exp            pcm_s16be_planar        wrapped_avframe
eightsvx_fib            pcm_s16le               ws_snd1
escape124               pcm_s16le_planar        xan_dpcm
escape130               pcm_s24be               xan_wc3
evrc                    pcm_s24daud             xan_wc4
exr                     pcm_s24le               xbin
fastaudio               pcm_s24le_planar        xbm
ffv1                    pcm_s32be               xface
ffvhuff                 pcm_s32le               xl
ffwavesynth             pcm_s32le_planar        xma1
fic                     pcm_s64be               xma2
fits                    pcm_s64le               xpm
flac                    pcm_s8                  xsub
flashsv                 pcm_s8_planar           xwd
flashsv2                pcm_sga                 y41p
flic                    pcm_u16be               ylc
flv                     pcm_u16le               yop
fmvc                    pcm_u24be               yuv4
fourxm                  pcm_u24le               zero12v
fraps                   pcm_u32be               zerocodec
frwu                    pcm_u32le               zlib
ftr                     pcm_u8                  zmbv

Enabled encoders:
a64multi                hevc_vaapi              pcm_s8_planar
a64multi5               huffyuv                 pcm_u16be
aac                     jpeg2000                pcm_u16le
aac_mf                  jpegls                  pcm_u24be
ac3                     libaom_av1              pcm_u24le
ac3_fixed               libcodec2               pcm_u32be
ac3_mf                  libgsm                  pcm_u32le
adpcm_adx               libgsm_ms               pcm_u8
adpcm_argo              libilbc                 pcm_vidc
adpcm_g722              libjxl                  pcx
adpcm_g726              libmp3lame              pfm
adpcm_g726le            libopencore_amrnb       pgm
adpcm_ima_alp           libopenjpeg             pgmyuv
adpcm_ima_amv           libopus                 phm
adpcm_ima_apm           librav1e                png
adpcm_ima_qt            libshine                ppm
adpcm_ima_ssi           libspeex                prores
adpcm_ima_wav           libsvtav1               prores_aw
adpcm_ima_ws            libtheora               prores_ks
adpcm_ms                libtwolame              qoi
adpcm_swf               libvo_amrwbenc          qtrle
adpcm_yamaha            libvorbis               r10k
alac                    libvpx_vp8              r210
alias_pix               libvpx_vp9              ra_144
amv                     libwebp                 rawvideo
anull                   libwebp_anim            roq
apng                    libx264                 roq_dpcm
aptx                    libx264rgb              rpza
aptx_hd                 libx265                 rv10
ass                     libxavs2                rv20
asv1                    libxeve                 s302m
asv2                    libxvid                 sbc
av1_amf                 ljpeg                   sgi
av1_nvenc               magicyuv                smc
av1_qsv                 mjpeg                   snow
av1_vaapi               mjpeg_qsv               sonic
avrp                    mjpeg_vaapi             sonic_ls
avui                    mlp                     speedhq
bitpacked               movtext                 srt
bmp                     mp2                     ssa
cfhd                    mp2fixed                subrip
cinepak                 mp3_mf                  sunrast
cljr                    mpeg1video              svq1
comfortnoise            mpeg2_qsv               targa
dca                     mpeg2_vaapi             text
dfpwm                   mpeg2video              tiff
dnxhd                   mpeg4                   truehd
dpx                     msmpeg4v2               tta
dvbsub                  msmpeg4v3               ttml
dvdsub                  msrle                   utvideo
dvvideo                 msvideo1                v210
dxv                     nellymoser              v308
eac3                    opus                    v408
exr                     pam                     v410
ffv1                    pbm                     vbn
ffvhuff                 pcm_alaw                vc2
fits                    pcm_bluray              vnull
flac                    pcm_dvd                 vorbis
flashsv                 pcm_f32be               vp8_vaapi
flashsv2                pcm_f32le               vp9_qsv
flv                     pcm_f64be               vp9_vaapi
g723_1                  pcm_f64le               wavpack
gif                     pcm_mulaw               wbmp
h261                    pcm_s16be               webvtt
h263                    pcm_s16be_planar        wmav1
h263p                   pcm_s16le               wmav2
h264_amf                pcm_s16le_planar        wmv1
h264_mf                 pcm_s24be               wmv2
h264_nvenc              pcm_s24daud             wrapped_avframe
h264_qsv                pcm_s24le               xbm
h264_vaapi              pcm_s24le_planar        xface
hap                     pcm_s32be               xsub
hdr                     pcm_s32le               xwd
hevc_amf                pcm_s32le_planar        y41p
hevc_mf                 pcm_s64be               yuv4
hevc_nvenc              pcm_s64le               zlib
hevc_qsv                pcm_s8                  zmbv

Enabled hwaccels:
av1_d3d11va             hevc_dxva2              vc1_dxva2
av1_d3d11va2            hevc_nvdec              vc1_nvdec
av1_d3d12va             hevc_vaapi              vc1_vaapi
av1_dxva2               hevc_vulkan             vp8_nvdec
av1_nvdec               mjpeg_nvdec             vp8_vaapi
av1_vaapi               mjpeg_vaapi             vp9_d3d11va
av1_vulkan              mpeg1_nvdec             vp9_d3d11va2
h263_vaapi              mpeg2_d3d11va           vp9_d3d12va
h264_d3d11va            mpeg2_d3d11va2          vp9_dxva2
h264_d3d11va2           mpeg2_d3d12va           vp9_nvdec
h264_d3d12va            mpeg2_dxva2             vp9_vaapi
h264_dxva2              mpeg2_nvdec             wmv3_d3d11va
h264_nvdec              mpeg2_vaapi             wmv3_d3d11va2
h264_vaapi              mpeg4_nvdec             wmv3_d3d12va
h264_vulkan             mpeg4_vaapi             wmv3_dxva2
hevc_d3d11va            vc1_d3d11va             wmv3_nvdec
hevc_d3d11va2           vc1_d3d11va2            wmv3_vaapi
hevc_d3d12va            vc1_d3d12va

Enabled parsers:
aac                     dvdsub                  mpegaudio
aac_latm                evc                     mpegvideo
ac3                     flac                    opus
adx                     ftr                     png
amr                     g723_1                  pnm
av1                     g729                    qoi
avs2                    gif                     rv34
avs3                    gsm                     sbc
bmp                     h261                    sipr
cavsvideo               h263                    tak
cook                    h264                    vc1
cri                     hdr                     vorbis
dca                     hevc                    vp3
dirac                   ipu                     vp8
dnxhd                   jpeg2000                vp9
dolby_e                 jpegxl                  vvc
dpx                     misc4                   webp
dvaudio                 mjpeg                   xbm
dvbsub                  mlp                     xma
dvd_nav                 mpeg4video              xwd

Enabled demuxers:
aa                      idf                     pcm_f64le
aac                     iff                     pcm_mulaw
aax                     ifv                     pcm_s16be
ac3                     ilbc                    pcm_s16le
ac4                     image2                  pcm_s24be
ace                     image2_alias_pix        pcm_s24le
acm                     image2_brender_pix      pcm_s32be
act                     image2pipe              pcm_s32le
adf                     image_bmp_pipe          pcm_s8
adp                     image_cri_pipe          pcm_u16be
ads                     image_dds_pipe          pcm_u16le
adx                     image_dpx_pipe          pcm_u24be
aea                     image_exr_pipe          pcm_u24le
afc                     image_gem_pipe          pcm_u32be
aiff                    image_gif_pipe          pcm_u32le
aix                     image_hdr_pipe          pcm_u8
alp                     image_j2k_pipe          pcm_vidc
amr                     image_jpeg_pipe         pdv
amrnb                   image_jpegls_pipe       pjs
amrwb                   image_jpegxl_pipe       pmp
anm                     image_pam_pipe          pp_bnk
apac                    image_pbm_pipe          pva
apc                     image_pcx_pipe          pvf
ape                     image_pfm_pipe          qcp
apm                     image_pgm_pipe          qoa
apng                    image_pgmyuv_pipe       r3d
aptx                    image_pgx_pipe          rawvideo
aptx_hd                 image_phm_pipe          rcwt
aqtitle                 image_photocd_pipe      realtext
argo_asf                image_pictor_pipe       redspark
argo_brp                image_png_pipe          rka
argo_cvg                image_ppm_pipe          rl2
asf                     image_psd_pipe          rm
asf_o                   image_qdraw_pipe        roq
ass                     image_qoi_pipe          rpl
ast                     image_sgi_pipe          rsd
au                      image_sunrast_pipe      rso
av1                     image_svg_pipe          rtp
avi                     image_tiff_pipe         rtsp
avisynth                image_vbn_pipe          s337m
avr                     image_webp_pipe         sami
avs                     image_xbm_pipe          sap
avs2                    image_xpm_pipe          sbc
avs3                    image_xwd_pipe          sbg
bethsoftvid             imf                     scc
bfi                     ingenient               scd
bfstm                   ipmovie                 sdns
bink                    ipu                     sdp
binka                   ircam                   sdr2
bintext                 iss                     sds
bit                     iv8                     sdx
bitpacked               ivf                     segafilm
bmv                     ivr                     ser
boa                     jacosub                 sga
bonk                    jpegxl_anim             shorten
brstm                   jv                      siff
c93                     kux                     simbiosis_imx
caf                     kvag                    sln
cavsvideo               laf                     smacker
cdg                     lc3                     smjpeg
cdxl                    libgme                  smush
cine                    libmodplug              sol
codec2                  libopenmpt              sox
codec2raw               live_flv                spdif
concat                  lmlm4                   srt
dash                    loas                    stl
data                    lrc                     str
daud                    luodat                  subviewer
dcstr                   lvf                     subviewer1
derf                    lxf                     sup
dfa                     m4v                     svag
dfpwm                   matroska                svs
dhav                    mca                     swf
dirac                   mcc                     tak
dnxhd                   mgsts                   tedcaptions
dsf                     microdvd                thp
dsicin                  mjpeg                   threedostr
dss                     mjpeg_2000              tiertexseq
dts                     mlp                     tmv
dtshd                   mlv                     truehd
dv                      mm                      tta
dvbsub                  mmf                     tty
dvbtxt                  mods                    txd
dxa                     moflex                  ty
ea                      mov                     usm
ea_cdata                mp3                     v210
eac3                    mpc                     v210x
epaf                    mpc8                    vag
evc                     mpegps                  vc1
ffmetadata              mpegts                  vc1t
filmstrip               mpegtsraw               vividas
fits                    mpegvideo               vivo
flac                    mpjpeg                  vmd
flic                    mpl2                    vobsub
flv                     mpsub                   voc
fourxm                  msf                     vpk
frm                     msnwc_tcp               vplayer
fsb                     msp                     vqf
fwse                    mtaf                    vvc
g722                    mtv                     w64
g723_1                  musx                    wady
g726                    mv                      wav
g726le                  mvi                     wavarc
g729                    mxf                     wc3
gdv                     mxg                     webm_dash_manifest
genh                    nc                      webvtt
gif                     nistsphere              wsaud
gsm                     nsp                     wsd
gxf                     nsv                     wsvqa
h261                    nut                     wtv
h263                    nuv                     wv
h264                    obu                     wve
hca                     ogg                     xa
hcom                    oma                     xbin
hevc                    osq                     xmd
hls                     paf                     xmv
hnm                     pcm_alaw                xvag
iamf                    pcm_f32be               xwma
ico                     pcm_f32le               yop
idcin                   pcm_f64be               yuv4mpegpipe

Enabled muxers:
a64                     h263                    pcm_s24be
ac3                     h264                    pcm_s24le
ac4                     hash                    pcm_s32be
adts                    hds                     pcm_s32le
adx                     hevc                    pcm_s8
aea                     hls                     pcm_u16be
aiff                    iamf                    pcm_u16le
alp                     ico                     pcm_u24be
amr                     ilbc                    pcm_u24le
amv                     image2                  pcm_u32be
apm                     image2pipe              pcm_u32le
apng                    ipod                    pcm_u8
aptx                    ircam                   pcm_vidc
aptx_hd                 ismv                    psp
argo_asf                ivf                     rawvideo
argo_cvg                jacosub                 rcwt
asf                     kvag                    rm
asf_stream              latm                    roq
ass                     lc3                     rso
ast                     lrc                     rtp
au                      m4v                     rtp_mpegts
avi                     matroska                rtsp
avif                    matroska_audio          sap
avm2                    md5                     sbc
avs2                    microdvd                scc
avs3                    mjpeg                   segafilm
bit                     mkvtimestamp_v2         segment
caf                     mlp                     smjpeg
cavsvideo               mmf                     smoothstreaming
chromaprint             mov                     sox
codec2                  mp2                     spdif
codec2raw               mp3                     spx
crc                     mp4                     srt
dash                    mpeg1system             stream_segment
data                    mpeg1vcd                streamhash
daud                    mpeg1video              sup
dfpwm                   mpeg2dvd                swf
dirac                   mpeg2svcd               tee
dnxhd                   mpeg2video              tg2
dts                     mpeg2vob                tgp
dv                      mpegts                  truehd
eac3                    mpjpeg                  tta
evc                     mxf                     ttml
f4v                     mxf_d10                 uncodedframecrc
ffmetadata              mxf_opatom              vc1
fifo                    null                    vc1t
filmstrip               nut                     voc
fits                    obu                     vvc
flac                    oga                     w64
flv                     ogg                     wav
framecrc                ogv                     webm
framehash               oma                     webm_chunk
framemd5                opus                    webm_dash_manifest
g722                    pcm_alaw                webp
g723_1                  pcm_f32be               webvtt
g726                    pcm_f32le               wsaud
g726le                  pcm_f64be               wtv
gif                     pcm_f64le               wv
gsm                     pcm_mulaw               yuv4mpegpipe
gxf                     pcm_s16be
h261                    pcm_s16le

Enabled protocols:
async                   http                    rtmp
bluray                  httpproxy               rtmpe
cache                   https                   rtmps
concat                  icecast                 rtmpt
concatf                 ipfs_gateway            rtmpte
crypto                  ipns_gateway            rtmpts
data                    librist                 rtp
fd                      libsrt                  srtp
ffrtmpcrypt             libssh                  subfile
ffrtmphttp              libzmq                  tcp
file                    md5                     tee
ftp                     mmsh                    tls
gopher                  mmst                    udp
gophers                 pipe                    udplite
hls                     prompeg

Enabled filters:
a3dscope                ddagrab                 pal100bars
aap                     deband                  pal75bars
abench                  deblock                 palettegen
abitscope               decimate                paletteuse
acompressor             deconvolve              pan
acontrast               dedot                   perms
acopy                   deesser                 perspective
acrossfade              deflate                 phase
acrossover              deflicker               photosensitivity
acrusher                deinterlace_qsv         pixdesctest
acue                    deinterlace_vaapi       pixelize
addroi                  dejudder                pixscope
adeclick                delogo                  pp
adeclip                 denoise_vaapi           pp7
adecorrelate            derain                  premultiply
adelay                  deshake                 prewitt
adenorm                 deshake_opencl          prewitt_opencl
aderivative             despill                 procamp_vaapi
adrawgraph              detelecine              program_opencl
adrc                    dialoguenhance          pseudocolor
adynamicequalizer       dilation                psnr
adynamicsmooth          dilation_opencl         pullup
aecho                   displace                qp
aemphasis               dnn_classify            random
aeval                   dnn_detect              readeia608
aevalsrc                dnn_processing          readvitc
aexciter                doubleweave             realtime
afade                   drawbox                 remap
afdelaysrc              drawbox_vaapi           remap_opencl
afftdn                  drawgraph               removegrain
afftfilt                drawgrid                removelogo
afir                    drawtext                repeatfields
afireqsrc               drmeter                 replaygain
afirsrc                 dynaudnorm              reverse
aformat                 earwax                  rgbashift
afreqshift              ebur128                 rgbtestsrc
afwtdn                  edgedetect              roberts
agate                   elbg                    roberts_opencl
agraphmonitor           entropy                 rotate
ahistogram              epx                     rubberband
aiir                    eq                      sab
aintegral               equalizer               scale
ainterleave             erosion                 scale2ref
alatency                erosion_opencl          scale_cuda
alimiter                estdif                  scale_qsv
allpass                 exposure                scale_vaapi
allrgb                  extractplanes           scale_vulkan
allyuv                  extrastereo             scdet
aloop                   fade                    scharr
alphaextract            feedback                scroll
alphamerge              fftdnoiz                segment
amerge                  fftfilt                 select
ametadata               field                   selectivecolor
amix                    fieldhint               sendcmd
amovie                  fieldmatch              separatefields
amplify                 fieldorder              setdar
amultiply               fillborders             setfield
anequalizer             find_rect               setparams
anlmdn                  firequalizer            setpts
anlmf                   flanger                 setrange
anlms                   flip_vulkan             setsar
anoisesrc               flite                   settb
anull                   floodfill               sharpness_vaapi
anullsink               format                  shear
anullsrc                fps                     showcqt
apad                    framepack               showcwt
aperms                  framerate               showfreqs
aphasemeter             framestep               showinfo
aphaser                 freezedetect            showpalette
aphaseshift             freezeframes            showspatial
apsnr                   frei0r                  showspectrum
apsyclip                frei0r_src              showspectrumpic
apulsator               fspp                    showvolume
arealtime               fsync                   showwaves
aresample               gblur                   showwavespic
areverse                gblur_vulkan            shuffleframes
arls                    geq                     shufflepixels
arnndn                  gradfun                 shuffleplanes
asdr                    gradients               sidechaincompress
asegment                graphmonitor            sidechaingate
aselect                 grayworld               sidedata
asendcmd                greyedge                sierpinski
asetnsamples            guided                  signalstats
asetpts                 haas                    signature
asetrate                haldclut                silencedetect
asettb                  haldclutsrc             silenceremove
ashowinfo               hdcd                    sinc
asidedata               headphone               sine
asisdr                  hflip                   siti
asoftclip               hflip_vulkan            smartblur
aspectralstats          highpass                smptebars
asplit                  highshelf               smptehdbars
ass                     hilbert                 sobel
astats                  histeq                  sobel_opencl
astreamselect           histogram               sofalizer
asubboost               hqdn3d                  spectrumsynth
asubcut                 hqx                     speechnorm
asupercut               hstack                  split
asuperpass              hstack_qsv              spp
asuperstop              hstack_vaapi            sr
atadenoise              hsvhold                 ssim
atempo                  hsvkey                  ssim360
atilt                   hue                     stereo3d
atrim                   huesaturation           stereotools
avectorscope            hwdownload              stereowiden
avgblur                 hwmap                   streamselect
avgblur_opencl          hwupload                subtitles
avgblur_vulkan          hwupload_cuda           super2xsai
avsynctest              hysteresis              superequalizer
axcorrelate             identity                surround
azmq                    idet                    swaprect
backgroundkey           il                      swapuv
bandpass                inflate                 tblend
bandreject              interlace               telecine
bass                    interleave              testsrc
bbox                    join                    testsrc2
bench                   kerndeint               thistogram
bilateral               kirsch                  threshold
bilateral_cuda          ladspa                  thumbnail
biquad                  lagfun                  thumbnail_cuda
bitplanenoise           latency                 tile
blackdetect             lenscorrection          tiltandshift
blackframe              lensfun                 tiltshelf
blend                   libplacebo              tinterlace
blend_vulkan            libvmaf                 tlut2
blockdetect             life                    tmedian
blurdetect              limitdiff               tmidequalizer
bm3d                    limiter                 tmix
boxblur                 loop                    tonemap
boxblur_opencl          loudnorm                tonemap_opencl
bs2b                    lowpass                 tonemap_vaapi
bwdif                   lowshelf                tpad
bwdif_cuda              lumakey                 transpose
bwdif_vulkan            lut                     transpose_opencl
cas                     lut1d                   transpose_vaapi
ccrepack                lut2                    transpose_vulkan
cellauto                lut3d                   treble
channelmap              lutrgb                  tremolo
channelsplit            lutyuv                  trim
chorus                  mandelbrot              unpremultiply
chromaber_vulkan        maskedclamp             unsharp
chromahold              maskedmax               unsharp_opencl
chromakey               maskedmerge             untile
chromakey_cuda          maskedmin               uspp
chromanr                maskedthreshold         v360
chromashift             maskfun                 vaguedenoiser
ciescope                mcdeint                 varblur
codecview               mcompand                vectorscope
color                   median                  vflip
color_vulkan            mergeplanes             vflip_vulkan
colorbalance            mestimate               vfrdet
colorchannelmixer       metadata                vibrance
colorchart              midequalizer            vibrato
colorcontrast           minterpolate            vidstabdetect
colorcorrect            mix                     vidstabtransform
colorhold               monochrome              vif
colorize                morpho                  vignette
colorkey                movie                   virtualbass
colorkey_opencl         mpdecimate              vmafmotion
colorlevels             mptestsrc               volume
colormap                msad                    volumedetect
colormatrix             multiply                vpp_qsv
colorspace              negate                  vstack
colorspace_cuda         nlmeans                 vstack_qsv
colorspectrum           nlmeans_opencl          vstack_vaapi
colortemperature        nlmeans_vulkan          w3fdif
compand                 nnedi                   waveform
compensationdelay       noformat                weave
concat                  noise                   xbr
convolution             normalize               xcorrelate
convolution_opencl      null                    xfade
convolve                nullsink                xfade_opencl
copy                    nullsrc                 xfade_vulkan
corr                    openclsrc               xmedian
cover_rect              oscilloscope            xstack
crop                    overlay                 xstack_qsv
cropdetect              overlay_cuda            xstack_vaapi
crossfeed               overlay_opencl          yadif
crystalizer             overlay_qsv             yadif_cuda
cue                     overlay_vaapi           yaepblur
curves                  overlay_vulkan          yuvtestsrc
datascope               owdenoise               zmq
dblur                   pad                     zoneplate
dcshift                 pad_opencl              zoompan
dctdnoiz                pad_vaapi               zscale

Enabled bsfs:
aac_adtstoasc           h264_redundant_pps      pgs_frame_merge
av1_frame_merge         hapqa_extract           prores_metadata
av1_frame_split         hevc_metadata           remove_extradata
av1_metadata            hevc_mp4toannexb        setts
chomp                   imx_dump_header         showinfo
dca_core                media100_to_mjpegb      text2movsub
dts2pts                 mjpeg2jpeg              trace_headers
dump_extradata          mjpega_dump_header      truehd_core
dv_error_marker         mov2textsub             vp9_metadata
eac3_core               mpeg2_metadata          vp9_raw_reorder
evc_frame_merge         mpeg4_unpack_bframes    vp9_superframe
extract_extradata       noise                   vp9_superframe_split
filter_units            null                    vvc_metadata
h264_metadata           opus_metadata           vvc_mp4toannexb
h264_mp4toannexb        pcm_rechunk

Enabled indevs:
dshow                   lavfi                   vfwcap
gdigrab                 libcdio

Enabled outdevs:
caca                    sdl2

git-full external libraries' versions: 

AMF v1.4.32-14-ge1acd43
aom v3.9.0-157-g6f8189bb64
aribb24 v1.0.3-5-g5e9be27
aribcaption 1.1.1
AviSynthPlus v3.7.3-70-g2b55ba40
bs2b 3.1.0
chromaprint 1.5.1
codec2 1.2.0-102-g3d69c8d0
dav1d 1.4.2
davs2 1.7-1-gb41cf11
ffnvcodec n12.2.72.0-1-g9934f17
flite v2.2-55-g6c9f20d
freetype VER-2-13-2
frei0r v2.3.2-16-gfdc9f32
fribidi v1.0.14
gsm 1.0.22
harfbuzz 8.5.0-123-gee0c7d6b
ladspa-sdk 1.17
lame 3.100
lensfun v0.3.95-1456-gc7bb6cb3
libass 0.17.2-6-g85ff2b3
libcdio-paranoia 10.2
libgme 0.6.3
libilbc v3.0.4-346-g6adb26d4a4
libjxl v0.10-snapshot-159-g45e688cb
libopencore-amrnb 0.1.6
libopencore-amrwb 0.1.6
libplacebo v6.338.0-133-g9e1257c8
libsoxr 0.1.3
libssh 0.10.6
libtheora 1.1.1
libwebp v1.4.0-17-g45129ee0
oneVPL 2.11
OpenCL-Headers v2024.05.08-2-gc860bb5
openmpt libopenmpt-0.6.16-3-gef06a8e61
opus v1.5.2-11-g2554a89e
rav1e p20240521-3-g0548232
rist 0.2.10
rubberband v1.8.1
SDL prerelease-2.29.2-185-gc79e61680
shaderc v2024.1-1-gf59f0d1
shine 3.1.1
snappy 1.1.10
speex Speex-1.2.1-25-g117bcc0
srt v1.5.3-79-g38a3a16
SVT-AV1 v2.1.0-11-g1400dd0d
twolame 0.4.0
uavs3d v1.1-47-g1fd0491
VAAPI 2.22.0.
vidstab v1.1.1-11-gc8caf90
vmaf v3.0.0-81-gb24c3d68
vo-amrwbenc 0.1.3
vorbis v1.3.7-10-g84c02369
vpx v1.14.0-282-g495c4b596
vulkan-loader v1.3.285-10-gd3d530c
x264 v0.164.3191
x265 3.6-28-g8787e8702
xavs2 1.4
xevd 0.5.0
xeve 0.5.0
xvid v1.3.7
zeromq 4.3.5
zimg release-3.0.5-150-g7143181
zvbi v0.2.42-58-ga48ab3a

