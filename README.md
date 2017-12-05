# BubblePop

## Motivation

최근 들어 페이스북, 트위터, 인스타그램 등에서 뉴스를 소비하는 사용자가 늘어났다. Pew
Research Center가 시행한 설문조사 [1]에 따르면, 페이스북을 통해 뉴스를 소비하는 페이스북
사용자는 2013년 47%에서 2016년 66%로 증가했다. 소셜 미디어의 등장은 뉴스 소비 행태를
바꿔놓았는데, 이는 크게 두 가지 관점에서 변화했다. 첫째, 뉴스를 보도하는 채널의 숫자가
증가해 사용자가 모든 정보를 수용할 수 없다. 둘째, 정보 선택의 주체가 사용자에서 플랫폼으로
이전되었다.

이러한 지점에서, 플랫폼은 사용자의 입맛에 알맞은 뉴스를 큐레이션 하는 형태로 발전해왔다.
그 결과 뉴스피드에는 사용자의 성향과 일치하는 정보만이 게시되기 시작했다. 2015년에
페이스북 연구진에 의해 이루어진 연구 [2]는 페이스북 뉴스피드의 편향을 실증적으로 보여준다.
이들 연구에 따르면, 진보적인 사용자의 뉴스피드에서 보수적인 뉴스가 차지하는 비율은 25%
아래, 보수적인 사용자의 뉴스피드에서 진보적인 뉴스가 차지하는 비율은 35% 아래다.
페이스북뿐만이 아닌 현존하는 많은 플랫폼에서 이러한 ‘큐레이션 개인화’를 제공하고 있으며,
일부는 이를 강제하고 있다. 일라이 파리저 (Eli Pariser)는 ‘큐레이션 개인화에 의해 사용자가
마치 각각의 거품에 갇히게 되는 현상’을 ‘필터버블 (Filter bubble)’이라고 칭했다 [3].

알고리즘에 의한 큐레이션 개인화는 일견 편하고 효율적으로 보이지만, 다양성이라는 사회적
가치를 가꾸어나가는 데 그리 유리한 환경을 제공하지 않는다. 많은 연구자가 이를 지적하고,
투명한 알고리즘 공개를 요구하기도 한다 [4, 5].

하지만, 이러한 문제에 공감하고 해결할 의지를 가진 사람도, 현재의 플랫폼에서는 균형된 뉴스
소비를 할 수 없다. 균형된 뉴스 소비를 위해서는 추가적인 노력이 필요하며, 이것은 필터버블
문제 해결에 대한 공감대 형성에 장벽이 된다. 따라서, 이 장벽을 낮추기 위한 애플리케이션의
필요성이 제기되고 있다.

## Problem Statement

우리가 해결하고자 하는 문제는, ‘소셜 미디어 사용자가 특별한 노력 없이, 한 주제에 대해 여러
논조를 담은 뉴스를 소비할 수 있도록 하는 것’이다. 필터버블 문제 해결에 대해 공감하고, 균형
잡힌 뉴스 소비에 대한 의지가 있는 집단이 우리 애플리케이션의 사용자가 될 것으로 예상한다.

다음 절로 넘어가기 전에, 우리의 애플리케이션이 필터버블 문제를 직접 해결하고자 하는 것이
아님을 짚는다. 필터버블 문제는 플랫폼의 자정 노력과 사용자들의 인식 전환이 함께 이루어져야
해결되는 것이며, 우리의 애플리케이션은 사용자의 인식 전환에 초점을 맞춘다.

## Goal

우리는 이 문제를 해결하기 위해 페이스북 뉴스피드를 조정하는 크롬 익스텐션 ‘BubblePop’을
제안한다. 시간, 인력 등의 한계로 인해, 소셜 미디어는 페이스북으로, 브라우저는 크롬으로 타깃
사용자를 좁혔음을 덧붙인다.

BubblePop은 페이스북 뉴스피드에 뉴스 링크가 등장했을 경우, 이를 발견하고 해당 링크
주변에 같은 주제-다른 시각의 뉴스 링크를 제시해준다. 사용자는 단순하고 짧은 행동을 통해
익스텐션이 제공하는 뉴스를 확인하고 소비할 수 있다.

이를 통해, 이전에 제시했던 ‘플랫폼 내부에서의 손쉬운 뉴스 균형 소비’를 이룰 것으로
기대한다.

## Interface

![](https://raw.githubusercontent.com/todoaskit/BubblePop/master/resources/example.png)

## User Evaluation

User evaluation was conducted with seven participants, where two of them are working in news media, and the rest are students.

We conducted user survey after the users used BubblePop application around 15 minutes.

- “I was able to check out articles with various views with a single click, which helps me to see the politics with impartial point of view.” (P3)
- “By clicking only a single + button, which is very similar to the original UI of Facebook, I was able to read articles with differing perspectives. Moreover, this app provides not only hyperlinks to the related articles, but also headlines, part of text, and political view of each media represented by colors, which makes this product impressive.” (P5)
- “This product supports only few articles. If the service is applied to various sections of articles, this product will become more meaningful.” (P4)
- “The service seems to be limited to political section, although political view of a news media can be showed in other than political section.” (P5)
- “The program tends to be incorrect when a queried article is released very recently (about 1~2 hours ago).” (P7)


## [Release](https://github.com/todoaskit/BubblePop/releases)


## Reference

[1] [Pew Research Cetner, News Use Across Social Media Platforms 2016](http://www.journalism.org/2016/05/26/news-use-across-social-media-platforms-2016/)

[2] [Bakshy, Eytan, Solomon Messing, and Lada A. Adamic. "Exposure to ideologically diverse news and opinion on Facebook." Science 348.6239 (2015): 1130-1132.](http://science.sciencemag.org/content/348/6239/1130)

[3] Pariser, Eli. The filter bubble: What the Internet is hiding from you. Penguin UK, 2011.

[4] [Bozdag, Engin, and Jeroen van den Hoven. "Breaking the filter bubble: democracy and design." Ethics and Information Technology 17.4 (2015): 249-265.](https://link.springer.com/article/10.1007/s10676-015-9380-y)

[5] [El-Bermawy, Mostafa. "Your Filter Bubble is Destroying Democracy". Wired. Retrieved 6 March 2017.](https://www.wired.com/2016/11/filter-bubble-destroyingdemocracy/)
