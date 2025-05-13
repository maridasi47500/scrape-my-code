class SearchController < ApplicationController
  def posts
      @code=`python scrape_bing.py "#{params[:query]}" #{params[:language]} en`
  end
end
